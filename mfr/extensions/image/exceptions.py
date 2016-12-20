from mfr.core.exceptions import ExporterError


class PillowImageError(ExporterError):
    """The Image related errors raised from a :class:`mfr.extentions.image`
    and relating to the Pillow Library should inherit from PillowImageError
    """
