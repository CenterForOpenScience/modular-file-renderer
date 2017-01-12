from mfr.core.exceptions import RendererError


class JaspVersionError(RendererError):
    """The jasp related errors raised from a :class:`mfr.extentions.jasp` and
    relating to minimum data archive version should inherit from RendererError
    """

    def __init__(self, message, created_by: str, data_archive_version: str,
                 minimum_version: str, renderer_class: str, extension: str,
                 code=500):
        self.keen_data = {'created_by': created_by,
                          'data_archive_version': data_archive_version,
                          'minimum_version': minimum_version
                          }
        super().__init__(message, 'jasp_version', renderer_class,
                         extension, code=code)


class JaspFileCorruptError(RendererError):
    """The jasp related errors raised from a :class:`mfr.extentions.jasp` and
    relating to failure while consuming JASP file should inherit from RendererError
    """

    def __init__(self, message, name: str, reason: str, renderer_class: str,
                 extension: str, code=500):
        self.keen_data = {'name': name,
                          'reason': reason}
        super().__init__(message, 'jasp_file_corrupt', renderer_class,
                         extension, code=code)
