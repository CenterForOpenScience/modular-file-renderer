import abc

class FileMeta(abc.ABCMeta):
    
    def __init__(cls, name, bases, dct):
        super(FileMeta, cls).__init__(name, bases, dct)
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        if name != 'FileRenderer':
            cls.registry[name] = cls

class FileRenderer(object):

    __metaclass__ = FileMeta

    @abc.abstractmethod
    def detect(self, fp):
        """Detects whether a given file pointer
        can be rendered by this renderer.

        :param fp: File pointer
        :return: Can file be rendered? (bool)

        """
        pass

    @abc.abstractmethod
    def render(self, fp, path):
        """Renders a file to HTML.

        :param fp: File pointer
        :param path: Path to file
        :return: HTML rendition of file

        """
        pass
