

class PluginError(Exception):
    """The WaterButler related errors raised
    from a plugins should inherit from PluginError
    """

    def __init__(self, message, code=500, log_message=None):
        super().__init__(code)
        self.code = code
        self.log_message = log_message
        if isinstance(message, dict):
            self.data = message
            self.message = json.dumps(message)
        else:
            self.data = None
            self.message = message

    def __repr__(self):
        return '<{}({}, {})>'.format(self.__class__.__name__, self.code, self.message)


class RendererError(PluginError):
    """The MFR related errors raised
    from a :class:`mfr.core.renderer` should
    inherit from RendererError
    """


class ProviderError(PluginError):
    """The MFR related errors raised
    from a :class:`mfr.core.provider` should
    inherit from ProviderError
    """


class DownloadError(ProviderError):
    pass


class MetadataError(ProviderError):
    pass
