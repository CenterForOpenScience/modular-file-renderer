import abc
import asyncio
import time
from dataclasses import dataclass, field

from waterbutler.core.streams import StringStream
from waterbutler.core.utils import make_provider

from mfr.server import settings
from mfr.core.metrics import MetricsRecord
from mfr.core.provider import ProviderMetadata
from mfr.tasks.serializer import serializable


class BaseExporter(metaclass=abc.ABCMeta):

    def __init__(self, ext, source_file_path, output_file_path, format, metadata):

        """Initialize the base exporter.

        :param ext: the name of the extension to be exported
        :param source_file_path: the path of the input file
        :param output_file_path: the path of the output file
        :param format: the format of the exported file (e.g. 1200*1200.jpg)
        """

        self.ext = ext
        self.source_file_path = source_file_path
        self.output_file_path = output_file_path
        self.format = format
        self.metadata = metadata
        self.exporter_metrics = MetricsRecord('exporter')
        if self._get_module_name():
            self.metrics = self.exporter_metrics.new_subrecord(self._get_module_name())

        self.exporter_metrics.merge({
            'class': self._get_module_name(),
            'format': self.format,
            'source_path': str(self.source_file_path),
            'output_path': str(self.output_file_path),
            # 'error': 'error_t',
            # 'elapsed': 'elpased_t',
        })

    @abc.abstractmethod
    def export(self):
        pass

    def _get_module_name(self):
        return self.__module__ \
            .replace('mfr.extensions.', '', 1) \
            .replace('.export', '', 1)

@serializable
@dataclass
class BaseRenderer(metaclass=abc.ABCMeta):
    metadata: ProviderMetadata
    file_path: str
    url: str
    assets_url: str
    export_url: str
    renderer_metrics: MetricsRecord = field(default=None)
    metrics: MetricsRecord = field(default=None)

    def __post_init__(self):
        self.assets_url = f'{self.assets_url}/{self._get_module_name()}'
        self.renderer_metrics = MetricsRecord('renderer',)
        if self._get_module_name():
            self.metrics = self.renderer_metrics.new_subrecord(self._get_module_name())

        if name := self.metadata.name:
            self.cache_file_path_str = f'/export/{self.metadata.unique_key}.{name}'
        else:
            self.cache_file_path_str = f'/export/{self.metadata.unique_key}'

        self.renderer_metrics.merge({
            'class': self._get_module_name(),
            'ext': self.metadata.ext,
            'url': self.url,
            'export_url': self.export_url,
            'file_path': self.file_path,
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
    def cache_provider(self):
        return make_provider(
            settings.CACHE_PROVIDER_NAME,
            {},  # User information which can be left blank
            settings.CACHE_PROVIDER_CREDENTIALS,
            settings.CACHE_PROVIDER_SETTINGS
        )

    async def get_cache_file_path(self):
        return await self.cache_provider.validate_path(self.cache_file_path_str)

    @abc.abstractmethod
    def _render(self) -> str:
        pass

    async def render(self):
        if self.use_celery or self.cache_result:
            self.cache_file_path = await self.cache_provider.validate_path(self.cache_file_path_str)
        if not self.use_celery:
            rendition = await self.do_render()
            return StringStream(rendition)
        else:
            from mfr.tasks.render import render
            result = render.delay(self)
            for i in range(100 * 60 * 10):
                if not result.ready():
                    time.sleep(0.01)
                else:
                    return await self.cache_provider.download(self.cache_file_path)

            return None

    async def do_render(self):
        if self.use_celery or self.cache_result:
            file_path_task = asyncio.ensure_future(self.get_cache_file_path())
        rendition = await asyncio.get_running_loop().run_in_executor(None, self._render)
        if self.use_celery or self.cache_result:
            upload_task = asyncio.ensure_future(
                self.cache_provider.upload(
                    StringStream(rendition),
                    await file_path_task
                )
            )
            if self.use_celery:
                await upload_task
        return rendition

    @property
    @abc.abstractmethod
    def file_required(self):
        """Does the rendering html need the raw file content to display correctly?
        Syntax-highlighted text files do.  Standard image formats do not, since an <img> tag
        only needs a url to the file.
        """
        pass

    @property
    @abc.abstractmethod
    def cache_result(self) -> bool:
        pass

    @property
    def use_celery(self) -> bool:
        return False

    def _get_module_name(self):
        return self.__module__ \
            .replace('mfr.extensions.', '', 1) \
            .replace('.render', '', 1)
