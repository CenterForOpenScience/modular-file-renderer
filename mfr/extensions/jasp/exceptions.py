from mfr.core.exceptions import RendererError


class JaspRendererError(RendererError):

    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, renderer_class='jasp', **kwargs)


class JaspVersionError(JaspRendererError):
    """The jasp related errors raised from a :class:`mfr.extentions.jasp` and relating to minimum
    data archive version should throw or subclass JaspVersionError.
    """

    __TYPE = 'jasp_version'

    def __init__(self, message, *args, code: int=400, created_by: str='',
                 actual_version: str='', required_version: str='', **kwargs):
        super().__init__(message, *args, code=code, **kwargs)
        self.created_by = created_by
        self.actual_version = actual_version
        self.required_version = required_version
        self.attr_stack.append([self.__TYPE, {
            'created_by': self.created_by,
            'actual_version': self.actual_version,
            'required_version': self.required_version,
        }])


class JaspFileCorruptError(JaspRendererError):
    """The jasp related errors raised from a :class:`mfr.extentions.jasp` and relating to failure
    while consuming JASP files should inherit from JaspFileCorruptError
    """

    __TYPE = 'jasp_file_corrupt'

    def __init__(self, message, *args, code: int=400, corruption_type: str='',
                 reason: str='', **kwargs):
        super().__init__(message, *args, code=code, **kwargs)
        self.corruption_type = corruption_type
        self.reason = reason
        self.attr_stack.append([self.__TYPE, {
            'corruption_type': self.corruption_type,
            'reason': self.reason,
        }])
