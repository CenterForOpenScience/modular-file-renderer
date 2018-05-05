import abc
import asyncio

import uuid

import waterbutler
from waterbutler.core.streams import StringStream

from mfr.core import utils
from mfr.core.metrics import MetricsRecord
from mfr.server import settings


class Cacheable(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def cache_result(self):
        pass

class BaseExporter(metaclass=abc.ABCMeta):

    def __init__(self, metadata, input_stream, format):

        """Initialize the base exporter.

        :param ext: the name of the extension to be exported
        :param source_file_path: the path of the input file
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
        if self.exporter_name:
            cache_file_path_str = '/export/{}.{}'.format(self.cache_file_id, self.exporter_name)
        else:
            cache_file_path_str = '/export/{}'.format(self.cache_file_id)

        self.exporter_metrics = MetricsRecord('exporter')
        if self._get_module_name():
            self.metrics = self.exporter_metrics.new_subrecord(self._get_module_name())

    async def __call__(self):

        self.source_wb_path = await self.local_cache_provider.validate_path(
            '/export/{}'.format(self.source_file_id)
        )
        self.source_file_path = self.source_wb_path.full_path
        self.output_file_id = '{}.{}'.format(self.source_wb_path.name, self.format)
        self.output_wb_path = await self.local_cache_provider.validate_path(
            '/export/{}'.format(self.output_file_id)
        )
        self.output_file_path = self.output_wb_path.full_path
        self.exporter_metrics.merge({
            'class': self._get_module_name(),
            'format': self.format,
            'source_path': str(self.source_wb_path),
            'output_path': str(self.output_wb_path),
            # 'error': 'error_t',
            # 'elapsed': 'elpased_t',
        })

        # Put the file into the local cahe provider (local fs)
        await self.local_cache_provider.upload(
            self.input_stream,
            self.source_wb_path
        )

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
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.export)

        # Return a stream of the converted file
        return await self.write_to_stream()

    def __del__(self):
        self.output_fp.close()

    @abc.abstractmethod
    def export(self):
        pass

    async def write_to_stream(self):
        self.output_fp = open(self.output_file_path, 'rb')
        return waterbutler.core.streams.FileStreamReader(self.output_fp)

    def _get_module_name(self):
        return self.__module__ \
            .replace('mfr.extensions.', '', 1) \
            .replace('.export', '', 1)


class BaseRenderer(Cacheable, metaclass=abc.ABCMeta):

    def __init__(self, metadata, file_stream, url, assets_url, export_url):
        self.metadata = metadata
        self.file_stream = file_stream
        self.url = url
        self.assets_url = '{}/{}'.format(assets_url, self._get_module_name())
        self.export_url = export_url
        self.renderer_metrics = MetricsRecord('renderer')
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

    async def __call__(self):

        self.renderer_metrics.add('class', self._get_module_name())

        if self.file_required:
            self.source_file_path = await self.local_cache_provider.validate_path(
                '/render/{}'.format(self.source_file_id)
            )
            await self.local_cache_provider.upload(
                await self.provider.download(),
                self.source_file_path
            )
        else:
            self.metrics.add('source_file.upload.required', False)

        loop = asyncio.get_event_loop()
        rendition = await loop.run_in_executor(None, self.render)


        return StringStream(rendition)

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
