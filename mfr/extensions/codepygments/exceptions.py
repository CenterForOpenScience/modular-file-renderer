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


class FileDecodingError(RendererError):
    """The codepygments related errors raised from a
    :class:`mfr.extentions.codepygments` and relating to decoding of
    file to display should inherit from FileDecodingError
    """

    def __init__(self, message, original_exception, original_message,
                 renderer_class: str, extension: str, code: int=500):

        self.keen_data = {'message': message,
                          'original_exception': original_exception,
                          'original_message': original_message}

        super().__init__(message, 'file_decoding', renderer_class,
                         extension, code=code)
