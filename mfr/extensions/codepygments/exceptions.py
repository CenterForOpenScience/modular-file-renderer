from mfr.core.exceptions import RendererError


class FileTooLargeError(RendererError):
    """The codepygments related errors raised from a
    :class:`mfr.extentions.codepygments` and relating to limit on size of
    file to display should inherit from FileTooLargeError
    """

    def __init__(self, message, keen_data: dict ={}, code=500):
        super().__init__(message, code, keen_data=keen_data)
