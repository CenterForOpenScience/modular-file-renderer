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


class ExportHandler(core.BaseHandler):

    ALLOWED_METHODS = ['GET']

    @waterbutler.server.utils.coroutine
    def prepare(self):
        if self.request.method not in self.ALLOWED_METHODS:
            return

        yield from super().prepare()

        self.format = self.request.query_arguments['format'][0].decode('utf-8')
        self.cache_file_path = yield from self.cache_provider.validate_path('/export/{}.{}'.format(self.metadata.unique_key, self.format))
        self.source_file_path = yield from self.local_cache_provider.validate_path('/export/{}'.format(uuid.uuid4()))
        self.output_file_path = yield from self.local_cache_provider.validate_path('/export/{}.{}'.format(self.source_file_path.name, self.format))

    @waterbutler.server.utils.coroutine
    def get(self):
        """Export a file to the format specified via the associated extension library"""

        if settings.CACHE_ENABLED:
            try:
                cached_stream = yield from self.cache_provider.download(self.cache_file_path)
            except waterbutler.core.exceptions.DownloadError as e:
                assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
                logger.info('No cached file found; Starting export')
            else:
                logger.info('Cached file found; Sending downstream')
                # TODO: Set Content Disposition Header
                self._set_headers()
                return (yield from self.write_stream(cached_stream))

        yield from self.local_cache_provider.upload(
            (yield from self.provider.download()),
            self.source_file_path
        )

        exporter = utils.make_exporter(
            self.metadata.ext,
            self.metadata,
            self.source_file_path.full_path,
            self.output_file_path.full_path,
            self.format
        )

        loop = asyncio.get_event_loop()
        yield from loop.run_in_executor(None, exporter.export)

        with open(self.output_file_path.full_path, 'rb') as fp:
            self._set_headers()
            yield from self.write_stream(waterbutler.core.streams.FileStreamReader(fp))

    @waterbutler.server.utils.coroutine
    def on_finish(self):
        if self.request.method not in self.ALLOWED_METHODS:
            return

        if settings.CACHE_ENABLED:
            with open(self.output_file_path.full_path, 'rb') as fp:
                yield from self.cache_provider.upload(waterbutler.core.streams.FileStreamReader(fp), self.cache_file_path)

        try:
            os.remove(self.source_file_path.full_path)
        except FileNotFoundError:
            pass

        try:
            os.remove(self.output_file_path.full_path)
        except FileNotFoundError:
            pass

    def _set_headers(self):
        self.set_header('Content-Disposition', 'attachment;filename="{}"'.format('{}.{}'.format(self.metadata.name.replace('"', '\\"'), self.format)))
        if self.metadata.content_type:
            self.set_header('Content-Type', self.metadata.content_type)
