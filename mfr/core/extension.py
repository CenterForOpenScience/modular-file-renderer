import abc


class BaseExporter(metaclass=abc.ABCMeta):

    def __init__(self, url, file_path, assets_url, ext):
        self.url = url
        self.file_path = file_path
        self.assets_url = '{}/{}'.format(assets_url, self._get_module_name())
        self.extension = ext

    @abc.abstractmethod
    def export(self):
        pass

    def _get_module_name(self):
        return self.__module__ \
            .replace('mfr.extensions.', '', 1) \
            .replace('.export', '', 1)


class BaseRenderer(metaclass=abc.ABCMeta):

    def __init__(self, url, download_url, file_path, assets_url, ext):
        self.url = url
        self.download_url = download_url
        self.file_path = file_path
        self.assets_url = '{}/{}'.format(assets_url, self._get_module_name())
        self.extension = ext

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractproperty
    def requires_file(self):
        pass

    def _get_module_name(self):
        return self.__module__ \
            .replace('mfr.extensions.', '', 1) \
            .replace('.render', '', 1)
