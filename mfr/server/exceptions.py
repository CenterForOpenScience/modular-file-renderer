class MFRHTTPError(Exception):
    """Base class for all expected error to be raised in mrf.server
    contains functions for creating user friendly responses"""

    def __init__(self, msg, code=500):
        super().__init__(msg)
        self._code = code

    @property
    def status_code(self):
        """HTTP Status code of this response"""
        return self._code

    def as_html(self):
        raise NotImplementedError


class LockedCodeError(MFRHTTPError):
    """Base class for constant status code error messages"""
    status_code = 500

    def __init__(self, msg):
        super().__init__(code=self.__class__.status_code)


class UnauthorizeError(LockedCodeError):
    status_code = 401

    def as_html(self):
        return """Whoops! Looks like you are not authorized to view this file"""


class ForbidenError(LockedCodeError):
    status_code = 403

    def as_html(self):
        return """Whoops! Looks like you don't have the
            correct permissions to view this file"""

class GoneError(LockedCodeError):
    status_code = 410

    def as_html(self):
        return """Whoops! Looks like you don't have the
            correct permissions to view this file"""

class NotFoundError(LockedCodeError):
    status_code = 404

    def as_html(self):
        return """Whoops! Looks like you don't have the
            correct permissions to view this file"""
