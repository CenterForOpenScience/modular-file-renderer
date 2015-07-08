import os
import uuid
import asyncio
import logging

import tornado.gen

import waterbutler.core.streams
import waterbutler.core.exceptions

from mfr.server import settings
from mfr.core import utils as utils
from mfr.server.handlers import core

logger = logging.getLogger(__name__)


class RenderHandler(core.BaseHandler):

    ALLOWED_METHODS = ['GET']
    extra = {
        'md5': ''
    }
    md5 = ''

    @tornado.gen.coroutine
    def prepare(self):
        if self.request.method not in self.ALLOWED_METHODS:
            return

        yield super().prepare()

        self.cache_file_path = yield from self.cache_provider.validate_path('/render/' + self.metadata.unique_key)
        self.source_file_path = yield from self.local_cache_provider.validate_path('/render/' + str(uuid.uuid4()))

    @tornado.gen.coroutine
    def get(self):
        """Render a file with the extension"""
        renderer = utils.make_renderer(
            self.metadata.ext,
            self.metadata,
            self.source_file_path.full_path,
            self.url,
            '{}://{}/assets'.format(self.request.protocol, self.request.host),
            self.request.uri.replace('/render?', '/export?', 1),
            extra = self.extra
        )

        #TO DO: attempt to grab md5 from watebutler

        if renderer.cache_result and settings.CACHE_ENABLED:
            try:
                cached_stream = yield from self.cache_provider.download(self.cache_file_path)
            except waterbutler.core.exceptions.DownloadError as e:
                assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
                logger.info('No cached file found; Starting render [{}]'.format(self.cache_file_path))
            else:
                logger.info('Cached file found; Sending downstream [{}]'.format(self.cache_file_path))
                return (yield self.write_stream(cached_stream))

        if renderer.file_required or self.md5 == '':
            download_stream = yield from self.provider.download()
            yield from self.local_cache_provider.upload(
                download_stream,
                self.source_file_path
            )
            self.md5 = download_stream.writers['md5'].hexdigest

        renderer.extra['md5'] = self.md5

        loop = asyncio.get_event_loop()
        rendition = (yield from loop.run_in_executor(None, renderer.render))

        # Spin off upload into non-blocking operation
        if renderer.cache_result and settings.CACHE_ENABLED:
            loop.call_soon(
                asyncio.async,
                self.cache_provider.upload(waterbutler.core.streams.StringStream(rendition), self.cache_file_path)
            )

        yield self.write_stream(waterbutler.core.streams.StringStream(rendition))

    @tornado.gen.coroutine
    def on_finish(self):
        if self.request.method not in self.ALLOWED_METHODS:
            return

        try:
            os.remove(self.source_file_path.full_path)
        except FileNotFoundError:
            pass
