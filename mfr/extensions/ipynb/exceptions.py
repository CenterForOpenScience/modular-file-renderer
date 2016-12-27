from mfr.core.exceptions import RendererError


class InvalidFormatError(RendererError):

    def __init__(self, message, download_url: str, original_exception: str,
                 original_message: str, renderer_class: str, extension: str,
                 code: int=500):

        self.keen_data = {'download_url': download_url,
                          'original_exception': original_exception,
                          'original_message': original_message}

        super().__init__(message, 'invalid_format', renderer_class,
                         extension, code=code)
