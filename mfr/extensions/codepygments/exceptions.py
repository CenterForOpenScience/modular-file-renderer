from mfr.core.exceptions import RendererError


class FileTooLargeError(RendererError):
    """The codepygments related errors raised from a
    :class:`mfr.extentions.codepygments` and relating to limit on size of
    file to display should inherit from FileTooLargeError
    """

    def __init__(self, message, file_size: int, max_size: int,
                 renderer_class: str, extension: str, code: int=500):

        self.keen_data = {'file_size': file_size,
                          'max_size': max_size}

        super().__init__(message, 'file_too_large', renderer_class,
                         extension, code=code)
