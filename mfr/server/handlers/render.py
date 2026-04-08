import http
import os
import logging

import waterbutler.core.streams
import waterbutler.core.exceptions

from mfr.server import settings
from mfr.core import utils as utils
from mfr.server.handlers import core


logger = logging.getLogger(__name__)


class RenderHandler(core.BaseHandler):

    NAME = 'render'
    ALLOWED_METHODS = ['GET']

    async def prepare(self):
        if self.request.method not in self.ALLOWED_METHODS:
            return

        await super().prepare()

        self.renderer_name = utils.get_renderer_name(self.metadata.ext)

        self.cache_file_id = self.metadata.unique_key

        if self.renderer_name:
            cache_file_path_str = f'/export/{self.cache_file_id}.{self.renderer_name}'
        else:
            cache_file_path_str = f'/export/{self.cache_file_id}'
        self.cache_file_path = await self.cache_provider.validate_path(cache_file_path_str)

        self.source_file_path = await self.local_cache_provider.validate_path(
            f'/render/{self.source_file_id}'
        )

    async def get(self):
        """Return HTML that will display the given file."""
        renderer = utils.make_renderer(
            self.metadata.ext,
            self.metadata,
            self.source_file_path.full_path,
            self.url,
            f'{self.request.protocol}://{self.request.host}/assets',
            self.request.uri.replace('/render?', '/export?', 1)
        )

        self.extension_metrics.add('class', renderer._get_module_name())

        if renderer.cache_result and settings.CACHE_ENABLED:
            try:
                cached_stream = await self.cache_provider.download(self.cache_file_path)
            except waterbutler.core.exceptions.DownloadError as e:
                assert e.code == 404, f'Non-404 DownloadError {e!r}'
                logger.info(f'No cached file found; Starting render [{self.cache_file_path}]')
                self.metrics.add('cache_file.result', 'miss')
            else:
                logger.info(f'Cached file found; Sending downstream [{self.cache_file_path}]')
                self.metrics.add('cache_file.result', 'hit')
                return await self.write_stream(cached_stream)

        if renderer.file_required:
            await self.local_cache_provider.upload(
                await self.provider.download(),
                self.source_file_path
            )
        else:
            self.metrics.add('source_file.upload.required', False)

        rendition = await renderer.render()
        self.renderer_metrics = renderer.renderer_metrics
        if rendition:
            await self.write_stream(rendition)
        else:
            self.set_status(http.HTTPStatus.ACCEPTED)
            self.write("Accepted")
            await self.flush()

    async def _cache_and_clean(self):
        if hasattr(self, 'source_file_path'):
            try:
                os.remove(self.source_file_path.full_path)
            except FileNotFoundError:
                pass
