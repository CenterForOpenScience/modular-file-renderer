import waterbutler.core.exceptions


class PluginError(waterbutler.core.exceptions.PluginError):
    """The MFR related errors raised from a plugin
    should inherit from PluginError
    """

    def as_html(self):
        return '''
            <link rel="stylesheet" href="/static/css/bootstrap.min.css">
            <div class="alert alert-warning" role="alert">{}</div>
            <div style="display: none;">This text and the text below is only presented because IE consumes error messages below 512 bytes</div>
            <div style="display: none;">Want to help save science? Want to get paid to develop free, open source software? Check out our openings!</div>
            '''.format(self.message)


class ExtensionError(PluginError):
    """The MFR related errors raised
    from a :class:`mfr.core.extension` should
    inherit from ExtensionError
    """


class RendererError(ExtensionError):
    """The MFR related errors raised
    from a :class:`mfr.core.extension` and relating
    to rendering should inherit from RendererError
    """


class ExporterError(ExtensionError):
    """The MFR related errors raised
    from a :class:`mfr.core.extension` and relating
    to exporting should inherit from ExporterError
    """


class ProviderError(PluginError):
    """The MFR related errors raised
    from a :class:`mfr.core.provider` should
    inherit from ProviderError
    """


class DownloadError(ProviderError):
    """The MFR related errors raised
    from a :class:`mfr.core.provider` and relating
    to downloads should inherit from DownloadError
    """


class MetadataError(ProviderError):
    """The MFR related errors raised
    from a :class:`mfr.core.provider` and relating
    to metadata should inherit from MetadataError
    """
