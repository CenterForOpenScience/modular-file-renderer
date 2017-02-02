from mfr.core.exceptions import RendererError


class InvalidFormatError(RendererError):

    __TYPE = 'ipynb_invalid_format'

    def __init__(self, message, *args, code: int=400, download_url: str='',
                 original_exception: Exception=None, **kwargs):
        super().__init__(message, *args, code=code, renderer_class='ipynb', **kwargs)

        self.download_url = download_url,
        self.original_exception = self._format_original_exception(original_exception)

        self.attr_stack.append([self.__TYPE, {
            'download_url': self.download_url,
            'original_exception': self.original_exception,
        }])
