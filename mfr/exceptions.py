# -*- coding: utf-8 -*-
"""Exception classes for the mfr package."""


class MFRError(Exception):
    """Base exception from which all MFR-related errors inherit."""
    pass


class ConfigurationError(MFRError):
    """Error raised when MFR is improperly configured."""
    pass


class RenderError(MFRError):
    """Base exception for all rendering related errors"""
    pass
