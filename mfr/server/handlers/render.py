import os
import uuid
import asyncio
import logging

import waterbutler.core.streams
import waterbutler.server.utils
import waterbutler.core.exceptions

from mfr.server import settings
from mfr.core import utils as utils
from mfr.server.handlers import core

logger = logging.getLogger(__name__)


class RenderHandler(core.BaseHandler):

    @waterbutler.server.utils.coroutine
    def prepare(self):
        yield from super().prepare()

    @waterbutler.server.utils.coroutine
    def get(self):
        """Render a file with the extension"""
        self.unique_path = yield from self.cache_provider.validate_path('/render/' + self.unique_key)
        self.local_cache_path = yield from self.local_cache_provider.validate_path('/render/' + str(uuid.uuid4()))
        self.renderer = utils.make_renderer(
            self.ext,
            self.url,
            self.download_url,
            self.local_cache_path.full_path,
            '{}://{}/assets'.format(self.request.protocol, self.request.host),
            self.ext
        )

        if self.renderer.cache_result and settings.CACHE_ENABLED:
            try:
                cached_stream = yield from self.cache_provider.download(self.unique_path)
            except waterbutler.core.exceptions.DownloadError as e:
                assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
                logger.info('No cached file found; Starting render')
            else:
                logger.info('Cached file found; Sending downstream')
                # TODO: Set Content Disposition Header
                return (yield from self.write_stream(cached_stream))

        if self.renderer.file_required:
            yield from self.local_cache_provider.upload(
                (yield from self.provider.download()),
                self.local_cache_path
            )

        loop = asyncio.get_event_loop()
        rendition = (yield from loop.run_in_executor(None, self.renderer.render))

        if self.renderer.file_required:
            try:
                os.remove(self.local_cache_path.full_path)
            except FileNotFoundError:
                pass

        # Spin off upload into non-blocking operation
        if self.renderer.cache_result and settings.CACHE_ENABLED:
            loop.call_soon(
                asyncio.async,
                self.cache_provider.upload(waterbutler.core.streams.StringStream(rendition), self.unique_path)
            )

        yield from self.write_stream(waterbutler.core.streams.StringStream(rendition))
