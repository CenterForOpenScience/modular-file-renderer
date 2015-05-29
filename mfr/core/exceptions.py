import waterbutler.core.exceptions


class PluginError(waterbutler.core.exceptions.PluginError):

    def as_html(self):
        return '''
            <div class="alert alert-warning" role="alert">{}</div>
            '''.format(self.message)


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
