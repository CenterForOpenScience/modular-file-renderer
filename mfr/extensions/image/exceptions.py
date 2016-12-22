from mfr.core.exceptions import ExporterError


class PillowImageError(ExporterError):
    """The Image related errors raised from a :class:`mfr.extentions.image`
    and relating to the Pillow Library should inherit from PillowImageError
    """

    def __init__(self, message, file_name_ext, imghdr_type, original_message,
                 original_exception, exporter_class: str, extension: str,
                 code: int=500):

        self.keen_data = {'file_name_ext': file_name_ext,
                          'imghdr_type': imghdr_type,
                          'original_message': original_message,
                          'original_exception': original_exception}

        super().__init__(message, 'pillow_image', exporter_class, extension,
                         code=code)
