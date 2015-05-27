import waterbutler.core.exceptions


class RendererError(waterbutler.core.exceptions.PluginError):
    """The MFR related errors raised
    from a :class:`mfr.core.renderer` should
    inherit from RendererError
    """


class ProviderError(waterbutler.core.exceptions.PluginError):
    """The MFR related errors raised
    from a :class:`mfr.core.provider` should
    inherit from ProviderError
    """


class DownloadError(ProviderError):
    pass


class MetadataError(ProviderError):
    pass
