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

    def __init__(self, message, driver_args: dict, extension: str, code=500):
        self.keen_data = {'driver_args': driver_args}
        super().__init__(message, 'make_renderer', extension, code=code)


class ExporterError(ExtensionError):
    """The MFR related errors raised
    from a :class:`mfr.core.extension` and relating
    to exporting should inherit from ExporterError
    """

    def __init__(self, message, nomen: str, exporter_class: str,
                 extension: str, code=500):
        self.keen_data = {'nomen': nomen,
                          'exporter_class': exporter_class,
                          'exporter_{}'.format(nomen): self.keen_data
                          }
        super().__init__(message, 'exporter', extension, code=code)


class SubprocessError(ExporterError):
    """The MFR related errors raised
    from a :class:`mfr.core.extension` and relating
    to subprocess should inherit from SubprocessError
    """

    def __init__(self, message, type: str, cmd: str, returncode: int,
                 path: str, extension: str, exporter_class: str='',
                 code: int=500):
        self.keen_data = {'type': type,
                          'cmd': cmd,
                          'returncode': returncode,
                          'path': path}
        if exporter_class:
            super().__init__(message, 'subprocess', exporter_class, extension,
                             code=code)
        else:
            super(ExporterError, self).__init__(message, 'subprocess',
                                                 extension, code=code)


class MakeExporterError(ExtensionError):
    """The MFR related errors raised
    from a :def:`mfr.core.utils.make_exporter`
    should inherit from MakeExporterError
    """

    def __init__(self, message, driver_args: dict, extension: str, code=500):
        self.keen_data = {'driver_args': driver_args}
        super().__init__(message, 'make_exporter', extension, code=code)


class ProviderError(PluginError):
    """The MFR related errors raised
    from a :class:`mfr.core.provider` should
    inherit from ProviderError
    """

    def __init__(self, message, nomen: str, provider: str, code=500):
        self.keen_data = {'nomen': nomen,
                          'provider': provider,
                          'provider_{}'.format(nomen): self.keen_data
                          }
        super().__init__(message, 'provider', code=code)


class DownloadError(ProviderError):
    """The MFR related errors raised
    from a :class:`mfr.core.provider` and relating
    to downloads should inherit from DownloadError
    """

    def __init__(self, message, download_url: str, response: str,
                 provider: str, code=500):
        self.keen_data = {'download_url': download_url,
                          'response': response}
        super().__init__(message, 'download', provider, code=code)


class MetadataError(ProviderError):
    """The MFR related errors raised
    from a :class:`mfr.core.provider` and relating
    to metadata should inherit from MetadataError
    """

    def __init__(self, message, metadata_url: str, response: str,
                 provider: str, code=500):
        self.keen_data = {'metadata_url': metadata_url,
                          'response': response}
        super().__init__(message, 'metadata', provider, code=code)
