from mfr.core.exceptions import RendererError


class JaspVersionError(RendererError):
    """The jasp related errors raised from a :class:`mfr.extentions.jasp` and
    relating to minimum data archive version should inherit from RendererError
    """

    def __init__(self, message, keen_data: dict ={}, code=500):
        keen_data = {'JaspVersionError': keen_data}
        super().__init__(message, code, keen_data=keen_data)


class JaspFileCorruptError(RendererError):
    """The jasp related errors raised from a :class:`mfr.extentions.jasp` and
    relating to failure while consuming JASP file should inherit from RendererError
    """

    def __init__(self, message, keen_data: dict ={}, code=500):
        keen_data = {'JaspFileCorruptError': keen_data}
        super().__init__(message, code, keen_data=keen_data)
