import abc


class BaseProvider(metaclass=abc.ABCMeta):

    def __init__(self, url):
        self.url = url

    @abc.abstractmethod
    def metadata(self):
        pass

    @abc.abstractmethod
    def download(self):
        pass
