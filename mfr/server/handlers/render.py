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

    ALLOWED_METHODS = ['GET']

    @waterbutler.server.utils.coroutine
    def prepare(self):
        if self.request.method not in self.ALLOWED_METHODS:
            return

        yield from super().prepare()

        self.cache_file_path = yield from self.cache_provider.validate_path('/render/' + self.metadata.unique_key)
        self.source_file_path = yield from self.local_cache_provider.validate_path('/render/' + str(uuid.uuid4()))

    @waterbutler.server.utils.coroutine
    def get(self):
        """Render a file with the extension"""
        renderer = utils.make_renderer(
            self.metadata.ext,
            self.metadata,
            self.source_file_path.full_path,
            self.url,
            '{}://{}/assets'.format(self.request.protocol, self.request.host),
            self.request.uri.replace('/render?', '/export?', 1)
        )

        if renderer.cache_result and settings.CACHE_ENABLED:
            try:
                cached_stream = yield from self.cache_provider.download(self.cache_file_path)
            except waterbutler.core.exceptions.DownloadError as e:
                assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
                logger.info('No cached file found; Starting render')
            else:
                logger.info('Cached file found; Sending downstream')
                return (yield from self.write_stream(cached_stream))

        if renderer.file_required:
            yield from self.local_cache_provider.upload(
                (yield from self.provider.download()),
                self.source_file_path
            )

        loop = asyncio.get_event_loop()
        rendition = (yield from loop.run_in_executor(None, renderer.render))

        # Spin off upload into non-blocking operation
        if renderer.cache_result and settings.CACHE_ENABLED:
            loop.call_soon(
                asyncio.async,
                self.cache_provider.upload(waterbutler.core.streams.StringStream(rendition), self.cache_file_path)
            )

        yield from self.write_stream(waterbutler.core.streams.StringStream(rendition))

    @waterbutler.server.utils.coroutine
    def on_finish(self):
        if self.request.method not in self.ALLOWED_METHODS:
            return

        try:
            os.remove(self.source_file_path.full_path)
        except FileNotFoundError:
            pass
