import abc


class BaseProvider(metaclass=abc.ABCMeta):

    def __init__(self, request, url):
        self.request = request
        self.url = url

    @abc.abstractmethod
    def metadata(self):
        pass

    @abc.abstractmethod
    def download(self):
        pass


class ProviderMetadata:

    def __init__(self, name, ext, content_type, unique_key, download_url):
        self.name = name
        self.ext = ext
        self.content_type = content_type
        self.unique_key = unique_key
        self.download_url = download_url
