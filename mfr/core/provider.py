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
