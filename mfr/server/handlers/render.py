import os
import asyncio
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
            cache_file_path_str = '/export/{}.{}'.format(self.cache_file_id, self.renderer_name)
        else:
            cache_file_path_str = '/export/{}'.format(self.cache_file_id)
        self.cache_file_path = await self.cache_provider.validate_path(cache_file_path_str)

        self.source_file_path = await self.local_cache_provider.validate_path(
            '/render/{}'.format(self.source_file_id)
        )

    async def get(self):
        """Return HTML that will display the given file."""
        renderer = utils.make_renderer(
            self.metadata.ext,
            self.metadata,
            self.source_file_path.full_path,
            self.url,
            '{}://{}/assets'.format(self.request.protocol, self.request.host),
            self.request.uri.replace('/render?', '/export?', 1)
        )

        self.extension_metrics.add('class', renderer._get_module_name())

        if renderer.cache_result and settings.CACHE_ENABLED:
            try:
                cached_stream = await self.cache_provider.download(self.cache_file_path)
            except waterbutler.core.exceptions.DownloadError as e:
                assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
                logger.info('No cached file found; Starting render [{}]'.format(self.cache_file_path))
                self.metrics.add('cache_file.result', 'miss')
            else:
                logger.info('Cached file found; Sending downstream [{}]'.format(self.cache_file_path))
                self.metrics.add('cache_file.result', 'hit')
                return await self.write_stream(cached_stream)

        if renderer.file_required:
            await self.local_cache_provider.upload(
                await self.provider.download(),
                self.source_file_path
            )
        else:
            self.metrics.add('source_file.upload.required', False)

        loop = asyncio.get_event_loop()
        rendition = await loop.run_in_executor(None, renderer.render)
        self.renderer_metrics = renderer.renderer_metrics

        # Spin off upload into non-blocking operation
        if renderer.cache_result and settings.CACHE_ENABLED:
            asyncio.ensure_future(
                self.cache_provider.upload(
                    waterbutler.core.streams.StringStream(rendition),
                    self.cache_file_path
                )
            )

        await self.write_stream(waterbutler.core.streams.StringStream(rendition))

    async def _cache_and_clean(self):
        if hasattr(self, 'source_file_path'):
            try:
                os.remove(self.source_file_path.full_path)
            except FileNotFoundError:
                pass
