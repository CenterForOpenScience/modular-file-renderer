from mfr.core.exceptions import RendererError

class CodePygmentsRendererError(RendererError):

    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, renderer_class='codepygments', **kwargs)


class FileTooLargeError(CodePygmentsRendererError):
    """The codepygments related errors raised from a :class:`mfr.extentions.codepygments` and
    relating to limit on size of file to display should inherit from FileTooLargeError
    """

    __TYPE = 'codepygments_file_too_large'

    def __init__(self, message, *args, code: int=400, file_size: int=None, max_size: int=None,
                 **kwargs):
        super().__init__(message, *args, code=code, **kwargs)

        self.file_size = file_size
        self.max_size = max_size

        self.attr_stack.append([self.__TYPE, {
            'file_size': self.file_size,
            'max_size': self.max_size
        }])


class FileDecodingError(CodePygmentsRendererError):
    """The codepygments related errors raised from a :class:`mfr.extentions.codepygments` and
    relating to decoding of file to display should inherit from FileDecodingError
    """

    __TYPE = 'codepygments_file_decoding'

    def __init__(self, message, *args, code: int=400, original_exception: Exception=None,
                 category: str='', **kwargs):
        super().__init__(message, *args, code=code, **kwargs)

        self.category = category
        self.original_exception = self._format_original_exception(original_exception)

        self.attr_stack.append([self.__TYPE, {
            'original_exception': self.original_exception,
            'category': self.category,
        }])
