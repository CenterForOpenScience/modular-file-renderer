import asyncio
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

        if self.exporter_name:
            cache_file_path_str = '/export/{}.{}'.format(self.cache_file_id, self.exporter_name)
        else:
            cache_file_path_str = '/export/{}'.format(self.cache_file_id)
        self.cache_file_path = await self.cache_provider.validate_path(cache_file_path_str)

        self.source_file_path = await self.local_cache_provider.validate_path(
            '/export/{}'.format(self.source_file_id)
        )

        self.output_file_id = '{}.{}'.format(self.source_file_path.name, self.format)
        self.output_file_path = await self.local_cache_provider.validate_path(
            '/export/{}'.format(self.output_file_id)
        )
        self.metrics.merge({
            'output_file': {
                'id': self.output_file_id,
                'path': str(self.output_file_path),
                'provider': self.local_cache_provider.NAME,
            }
        })

    async def get(self):
        """Export a file to the format specified via the associated extension library"""

        # File is already in the requested format
        if self.metadata.ext.lower() == ".{}".format(self.format.lower()):
            await self.write_stream(await self.provider.download())
            logger.info('Exported {} with no conversion.'.format(self.format))
            self.metrics.add('export.conversion', 'noop')
            return

        if settings.CACHE_ENABLED:
            try:
                cached_stream = await self.cache_provider.download(self.cache_file_path)
            except DownloadError as e:
                assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
                logger.info('No cached file found; Starting export [{}]'.format(self.cache_file_path))
                self.metrics.add('cache_file.result', 'miss')
            else:
                logger.info('Cached file found; Sending downstream [{}]'.format(self.cache_file_path))
                self.metrics.add('cache_file.result', 'hit')
                self._set_headers()
                return await self.write_stream(cached_stream)

        await self.local_cache_provider.upload(
            await self.provider.download(),
            self.source_file_path
        )

        exporter = utils.make_exporter(
            self.metadata.ext,
            self.source_file_path.full_path,
            self.output_file_path.full_path,
            self.format,
            self.metadata,
        )

        self.extension_metrics.add('class', exporter._get_module_name())

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, exporter.export)
        self.exporter_metrics = exporter.exporter_metrics

        with open(self.output_file_path.full_path, 'rb') as fp:
            self._set_headers()
            await self.write_stream(waterbutler.core.streams.FileStreamReader(fp))

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
