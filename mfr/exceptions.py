# -*- coding: utf-8 -*-
"""Exception classes for the mfr package."""


class MFRException(Exception):
    """Base exception from which all MFR-related errors inherit."""
    pass


class ConfigurationError(MFRException):
    """Error raised when MFR is improperly configured."""
    pass
