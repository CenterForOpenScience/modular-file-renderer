import abc


class BaseExporter(metaclass=abc.ABCMeta):

    def __init__(self, metadata, source_file_path, output_file_path, format):
        self.metadata = metadata
        self.source_file_path = source_file_path
        self.output_file_path = output_file_path
        self.format = format

    @abc.abstractmethod
    def export(self):
        pass

    def _get_module_name(self):
        return self.__module__ \
            .replace('mfr.extensions.', '', 1) \
            .replace('.export', '', 1)


class BaseRenderer(metaclass=abc.ABCMeta):

    def __init__(self, metadata, url, file_path, assets_url):
        self.metadata = metadata
        self.url = url
        self.file_path = file_path
        self.assets_url = '{}/{}'.format(assets_url, self._get_module_name())

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractproperty
    def file_required(self):
        pass

    @abc.abstractproperty
    def cache_result(self):
        pass

    def _get_module_name(self):
        return self.__module__ \
            .replace('mfr.extensions.', '', 1) \
            .replace('.render', '', 1)
