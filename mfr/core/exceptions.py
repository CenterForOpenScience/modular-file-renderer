import waterbutler.core.exceptions


class PluginError(waterbutler.core.exceptions.PluginError):
    """The MFR related errors raised from a plugin
    should inherit from PluginError
    """

    def __init__(self, message, nomen: str, code=500):
        super().__init__(message, code)
        self.nomen = nomen
        self.data = self.keen_data

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

    def __init__(self, message, nomen: str, extension: str, code=500):
        self.keen_data = {'nomen': nomen,
                          'extension': extension,
                          'extention_{}'.format(nomen): self.keen_data
                          }
        super().__init__(message, 'extension', code=code)


class RendererError(ExtensionError):
    """The MFR related errors raised
    from a :class:`mfr.core.extension` and relating
    to rendering should inherit from RendererError
    """

    def __init__(self, message, nomen: str, renderer_class: str,
                 extension: str, code=500):
        self.keen_data = {'nomen': nomen,
                          'renderer_class': renderer_class,
                          'renderer_{}'.format(nomen): self.keen_data
                          }
        super().__init__(message, 'renderer', extension, code=code)


class MakeRendererError(ExtensionError):
    """The MFR related errors raised
    from a :def:`mfr.core.utils.make_renderer`
    should inherit from MakeRendererError
    """


class ExporterError(ExtensionError):
    """The MFR related errors raised
    from a :class:`mfr.core.extension` and relating
    to exporting should inherit from ExporterError
    """

    def __init__(self, message, nomen: str, exporter_class: str,
                 extension: str, code=500):
        self.keen_data = {'nomen': nomen,
                          'exporter_class': exporter_class,
                          'expoorter_{}'.format(nomen): self.keen_data
                          }
        super().__init__(message, 'exporter', extension, code=code)


class SubprocessError(ExporterError):
    """The MFR related errors raised
    from a :class:`mfr.core.extension` and relating
    to subprocess should inherit from SubprocessError
    """


class MakeExporterError(ExtensionError):
    """The MFR related errors raised
    from a :def:`mfr.core.utils.make_exporter`
    should inherit from MakeExporterError
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
