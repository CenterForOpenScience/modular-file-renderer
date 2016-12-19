from mfr.core.exceptions import ExporterError


class PillowImageError(ExporterError):
    """The Image related errors raised from a :class:`mfr.extentions.image`
    and relating to the Pillow Library should inherit from PillowImageError
    """

    def __init__(self, message, keen_data: dict ={}, code=500):
        keen_data = {'PillowImageError': keen_data}
        super().__init__(message, code, keen_data=keen_data)
