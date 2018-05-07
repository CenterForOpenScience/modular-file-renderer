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

    async def get(self):
        """Return HTML that will display the given file."""

        # Make a render function that will return the rendered file as a string
        # when invoked
        render = utils.bind_render(
            self.metadata,
            await self.provider.download(),
            self.url,
            '{}://{}/assets'.format(self.request.protocol, self.request.host),
            self.request.uri.replace('/render?', '/export?', 1)
        )

        if render.cache_result and settings.CACHE_ENABLED:

            if self.renderer_name:
                cache_file_path_str = '/export/{}.{}'.format(self.cache_file_id, self.renderer_name)
            else:
                cache_file_path_str = '/export/{}'.format(self.cache_file_id)

            # Try and use a cached version of the render
            self.cache_file_path = await self.cache_provider.validate_path(cache_file_path_str)
            try:
                cached_stream = await self.cache_provider.download(self.cache_file_path)

            # No cached version of the render (skip else)
            except waterbutler.core.exceptions.DownloadError as e:
                assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
                logger.info('No cached file found; Starting render [{}]'.format(self.cache_file_path))
                self.metrics.add('cache_file.result', 'miss')

            # No exception; send the cached version
            else:
                logger.info('Cached file found; Sending downstream [{}]'.format(self.cache_file_path))
                self.metrics.add('cache_file.result', 'hit')
                return await self.write_stream(cached_stream)

        # Perform the render and write the result to the response
        rendition = await render()
        await self.write_stream(rendition)

        # Spin off upload of cached render into non-blocking operation
        if render.cache_result and settings.CACHE_ENABLED:
            asyncio.ensure_future(
                self.cache_provider.upload(
                    waterbutler.core.streams.StringStream(rendition),
                    self.cache_file_path
                )
            )
