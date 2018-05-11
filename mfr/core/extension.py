import abc
import asyncio
from os import remove
import uuid

import waterbutler
from waterbutler.core.streams import StringStream

from mfr.core import utils
from mfr.core.metrics import MetricsRecord
from mfr.server import settings


class BaseExporter(metaclass=abc.ABCMeta):

    def __init__(self, metadata, input_stream, format):
        """Initialize the base exporter.

        :param ext: the name of the extension to be exported
        :param input_stream: input file as a stream
        :param output_file_path: the path of the output file
        :param format: the format of the exported file (e.g. 1200*1200.jpg)
        """
        self.metadata = metadata
        self.ext = metadata.ext
        self.input_stream = input_stream
        self.format = format
        self.source_file_id = uuid.uuid4()
        self.cache_file_id = '{}.{}'.format(self.metadata.unique_key, self.format)
        self.local_cache_provider = waterbutler.core.utils.make_provider(
            'filesystem', {}, {}, settings.LOCAL_CACHE_PROVIDER_SETTINGS
        )
        self.exporter_name = utils.get_exporter_name(self.metadata.ext)
        self.exporter_metrics = MetricsRecord('exporter')
        if self._get_module_name():
            self.metrics = self.exporter_metrics.new_subrecord(self._get_module_name())

    async def __call__(self):
        """Returns a stream wrapping the exported version of the file.
        """
        self.output_file_id = '{}.{}'.format((await self.source_wb_path).name, self.format)
        self.output_wb_path = await self.local_cache_provider.validate_path(
            '/export/{}'.format(self.output_file_id)
        )
        self.output_file_path = self.output_wb_path.full_path
        self.exporter_metrics.merge({
            'class': self._get_module_name(),
            'format': self.format,
            'source_path': str(await self.source_wb_path),
            'output_path': str(self.output_wb_path),
            # 'error': 'error_t',
            # 'elapsed': 'elpased_t',
        })

        # Note where the output file is for diagnostics
        self.exporter_metrics.merge({
            'output_file': {
                'id': self.output_file_id,
                'path': str(self.output_wb_path),
                'provider': self.local_cache_provider.NAME,
            }
        })

        # Execute the extension's export method asynchronously and wait for it
        # to finish
        await self.export()

        # Return a stream of the converted file
        return self.write_to_stream()

    @property
    async def source_wb_path(self):
        """Validate a local filesystem path using the filesystem provider. Used
        to store a temporary file if it is needed by the exporter.
        """
        try:
            return self._source_wb_path
        except:
            self._source_wb_path = await self.local_cache_provider.validate_path(
                '/export/{}'.format(self.source_file_id)
            )
            return self._source_wb_path

    @property
    async def source_file_path(self):
        """Returns a path at which the source file is located. Ensures that the
        file is at the location
        """
        try:
            return self._source_file_path
        except:
            self._source_file_path = (await self.source_wb_path).full_path
            await self.local_cache_provider.upload(
                self.input_stream,
                await self.source_wb_path
            )
            return self._source_file_path

    def __del__(self):
        self.output_fp.close()

    @abc.abstractmethod
    def export(self):
        pass

    def write_to_stream(self):
        self.output_fp = open(self.output_file_path, 'rb')
        return waterbutler.core.streams.FileStreamReader(self.output_fp)

    def _get_module_name(self):
        return self.__module__ \
            .replace('mfr.extensions.', '', 1) \
            .replace('.export', '', 1)


class BaseRenderer(metaclass=abc.ABCMeta):

    def __init__(self, metadata, file_stream, url, assets_url, export_url):
        self.metadata = metadata
        self.file_stream = file_stream  # A future that resolves to a file stream
        self.url = url
        self.assets_url = '{}/{}'.format(assets_url, self._get_module_name())
        self.export_url = export_url
        self.renderer_metrics = MetricsRecord('renderer')
        self.source_file_id = uuid.uuid4()
        if self._get_module_name():
            self.metrics = self.renderer_metrics.new_subrecord(self._get_module_name())

        self.renderer_metrics.merge({
            'class': self._get_module_name(),
            'ext': self.metadata.ext,
            'url': self.url,
            'export_url': self.export_url,
            # 'file_path': self.file_path,
            # 'error': 'error_t',
            # 'elapsed': 'elpased_t',
        })

        # unoconv gets file_required and cache_result from its subrenderer, which is constructed
        # at the end of __init__
        try:
            self.renderer_metrics.add('file_required', self.file_required)
            self.renderer_metrics.add('cache_result', self.cache_result)
        except AttributeError:
            pass

    @property
    def local_cache_provider(self):
        if not self._local_cache_provider:
            self._local_cache_provider = waterbutler.core.utils.make_provider(
                'filesystem', {}, {}, settings.LOCAL_CACHE_PROVIDER_SETTINGS
            )
        return self._local_cache_provider

    async def get_source_file_path(self):
        if self._source_file_path is None:
            self._source_file_path = await self.local_cache_provider.validate_path(
                '/render/{}'.format(self.source_file_id)
            )
        return self._source_file_path

    async def __call__(self):

        self.renderer_metrics.add('class', self._get_module_name())

        if self.file_required:
            await self.local_cache_provider.upload(
                await self.file_stream,
                await self.source_file_path
            )
        else:
            self.metrics.add('source_file.upload.required', False)

        rendition = self.render()

        return StringStream(rendition)

    def __del(self):
        if self.file_required:
            try:
                remove(self._source_file_path.full_path)
            except FileNotFoundError:
                pass

    @abc.abstractproperty
    def cache_result(self):
        pass

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractproperty
    def file_required(self):
        """Does the rendering html need the raw file content to display correctly?
        Syntax-highlighted text files do.  Standard image formats do not, since an <img> tag
        only needs a url to the file.
        """
        pass

    def _get_module_name(self):
        return self.__module__ \
            .replace('mfr.extensions.', '', 1) \
            .replace('.render', '', 1)
