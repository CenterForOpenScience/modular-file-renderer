from mfr.core.exceptions import ExporterError


class PillowImageError(ExporterError):
    """The Image related errors raised from a :class:`mfr.extentions.pdf`
    and relating to the Pillow Library should inherit from PillowImageError
    """

    __TYPE = 'pdf_pillow'

    def __init__(self, message, *args, export_format: str='', detected_format: str='',
                 original_exception: Exception=None, **kwargs):
        super().__init__(message, *args, exporter_class='image', **kwargs)

        self.export_format = export_format
        self.detected_format = detected_format
        self.original_exception = self._format_original_exception(original_exception)

        self.attr_stack.append([self.__TYPE, {
            'export_format': self.export_format,
            'detected_format': self.detected_format,
            'original_exception': self.original_exception,
        }])
