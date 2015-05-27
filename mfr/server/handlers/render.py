import os
import asyncio
import logging

import waterbutler.core.exceptions
from waterbutler.providers.filesystem import FileSystemProvider

from mfr.core import utils as core_utils
from mfr.core.streams.base import StringStream

from mfr.server import utils
from mfr.server import settings
from mfr.server.handlers import core

from mfr.core.streams import FileStreamReader


logger = logging.getLogger(__name__)


class RenderHandler(core.BaseHandler):
    @utils.coroutine
    def prepare(self):
        yield from super().prepare()

    @asyncio.coroutine
    def write_stream(self, stream):
        while True:
            chunk = yield from stream.read(settings.CHUNK_SIZE)
            if not chunk:
                break
            self.write(chunk)
            yield from utils.future_wrapper(self.flush())

    @utils.coroutine
    def get(self):
        """Render a file with the extension"""
        try:
            cached_stream = yield from self.cache_provider.download(self.unique_path)
        except waterbutler.core.exceptions.DownloadError as e:
            assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
            logger.info('No cached file found; Starting render')
        else:
            logger.info('Cached file found; Sending downstream')
            return (yield from self.write_stream(cached_stream))

        yield from self.local_cache_provider.upload(
            (yield from self.provider.download()),
            self.local_cache_path
        )

        self.extension = core_utils.make_extension(
            self.ext,
            self.url,
            self.local_cache_path.full_path,
            '{}://{}/assets'.format(self.request.protocol, self.request.host),
            self.ext,
        )

        loop = asyncio.get_event_loop()
        rendition = (yield from loop.run_in_executor(None, self.extension.render))

        # TODO Spin off current request
        yield from self.cache_provider.upload(StringStream(rendition), self.unique_path)
        yield from self.write_stream(StringStream(rendition))
