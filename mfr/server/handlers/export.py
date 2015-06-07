import asyncio
import logging

import waterbutler.core.streams
import waterbutler.server.utils
import waterbutler.core.exceptions

from mfr.core import utils as utils
from mfr.server.handlers import core


logger = logging.getLogger(__name__)


class ExportHandler(core.BaseHandler):

    @waterbutler.server.utils.coroutine
    def prepare(self):
        yield from super().prepare()

    @waterbutler.server.utils.coroutine
    def get(self):
        """Export a file with the extension"""
        type = self.request.query_arguments['type'][0].decode('utf-8')
        unique_path = yield from self.cache_provider.validate_path('/export/{}.{}'.format(self.unique_key, type))
        local_cache_path = yield from self.local_cache_provider.validate_path('/export/{}.{}'.format(self.unique_key, type))

        try:
            cached_stream = yield from self.cache_provider.download('{}.{}'.format(unique_path, type))
        except waterbutler.core.exceptions.DownloadError as e:
            assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
            logger.info('No cached file found; Starting export')
        else:
            logger.info('Cached file found; Sending downstream')
            # TODO: Set Content Disposition Header
            return (yield from self.write_stream(cached_stream))

        self.extension = utils.make_exporter(
            self.ext,
            self.local_cache_path.full_path,
            self.ext,
            self.type
        )

        yield from self.local_cache_provider.upload(
            (yield from self.provider.download()),
            local_cache_path
        )

        loop = asyncio.get_event_loop()
        rendition = (yield from loop.run_in_executor(None, self.extension.export))

        # TODO Spin off current request
        yield from self.cache_provider.upload(waterbutler.core.streams.StringStream(rendition), unique_path)
        yield from self.write_stream(waterbutler.core.streams.StringStream(rendition))
