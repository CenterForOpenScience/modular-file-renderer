import logging
import os

from waterbutler.core.exceptions import InvalidParameters, DownloadError
import waterbutler.core.streams

from mfr.core import utils
from mfr.server import settings
from mfr.server.handlers import core

logger = logging.getLogger(__name__)


class ExportHandler(core.BaseHandler):

    NAME = 'export'
    ALLOWED_METHODS = ['GET']

    async def prepare(self):
        if self.request.method not in self.ALLOWED_METHODS:
            return

        await super().prepare()

        format = self.request.query_arguments.get('format', None)
        if not format:
            raise InvalidParameters("Invalid Request: Url requires query parameter 'format' with"
                                    " appropriate extension")
        # TODO: do we need to catch exceptions for decoding?
        self.format = format[0].decode('utf-8')
        self.exporter_name = utils.get_exporter_name(self.metadata.ext)

        self.cache_file_id = '{}.{}'.format(self.metadata.unique_key, self.format)

    async def get(self):
        """Export a file to the format specified via the associated extension
        library.


        First, try to export the file directly - this is only valid if the file is
        already in the correct format.

        Next, if caching is enabled, try to use a cached version.

        Finally, do the actual conversion and export the converted file.
        """

        self._set_headers()

        # File is already in the requested format
        if self.metadata.ext.lower() == ".{}".format(self.format.lower()):
            await self.write_stream(await self.provider.download())
            logger.info('Exported {} with no conversion.'.format(self.format))
            self.metrics.add('export.conversion', 'noop')
            return

        # Try to get a cached version
        if settings.CACHE_ENABLED:
            if self.exporter_name:
                cache_file_path_str = '/export/{}.{}'.format(self.cache_file_id, self.exporter_name)
            else:
                cache_file_path_str = '/export/{}'.format(self.cache_file_id)
            try:
                self.cache_file_path = await self.cache_provider.validate_path(cache_file_path_str)
                await self.write_stream(self.cache_provider.download(self.cache_file_path))
                logger.info('Cached file found; Sending downstream [{}]'.format(self.cache_file_path))
                self.metrics.add('cache_file.result', 'hit')
                return

            # Cache miss
            except DownloadError as e:
                assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
                logger.info('No cached file found; Starting export [{}]'.format(self.cache_file_path))
                self.metrics.add('cache_file.result', 'miss')

        # File isn't cached and it needs to be converted
        await self.write_stream(await utils.bind_convert(
            self.metadata,
            await self.provider.download(),
            self.format
        )())

    async def _cache_and_clean(self):
        if settings.CACHE_ENABLED and os.path.exists(self.output_file_path.full_path):
            with open(self.output_file_path.full_path, 'rb') as fp:
                await self.cache_provider.upload(waterbutler.core.streams.FileStreamReader(fp), self.cache_file_path)

        if hasattr(self, 'source_file_path'):
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
