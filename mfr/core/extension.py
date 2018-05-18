import abc

from mfr.core.metrics import MetricsRecord


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


class BaseRenderer(metaclass=abc.ABCMeta):

    def __init__(self, metadata, file_path, url, assets_url, export_url):
        self.metadata = metadata
        self.file_path = file_path
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

    @abc.abstractproperty
    def cache_result(self):
        pass

    def _get_module_name(self):
        return self.__module__ \
            .replace('mfr.extensions.', '', 1) \
            .replace('.render', '', 1)
