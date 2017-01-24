import waterbutler.core.exceptions

from mfr import settings


class PluginError(waterbutler.core.exceptions.PluginError):
    """The MFR related errors raised from a plugin should inherit from PluginError
    """

    __TYPE = 'plugin'

    def __init__(self, message, *args, code=500, **kwargs):
        super().__init__(message, code)
        self.attr_stack = [
            ['error', {'message': self.message, 'code': self.code}],
            [self.__TYPE, {}],
        ]

    def as_html(self):
        return '''
            <link rel="stylesheet" href="/static/css/bootstrap.min.css">
            <div class="alert alert-warning" role="alert">{}</div>
            <div style="display: none;">This text and the text below is only presented because
              IE consumes error messages below 512 bytes</div>
            <div style="display: none;">Want to help save science? Want to get paid to develop
              free, open source software? Check out our openings!</div>
        '''.format(self.message)

    def _format_original_exception(self, exc):
        """Sometimes we catch an error from an external library, but would like to throw our own
        error instead.  This method will take in an external error class and format it for
        consistent representation in the error metrics.
        """
        formatted_exc = {'class': '', 'message': ''}
        if exc is not None:
            formatted_exc['class'] = exc.__class__.__name__
            formatted_exc['message'] = str(exc)
        return formatted_exc


class ExtensionError(PluginError):
    """The MFR related errors raised from a :class:`mfr.core.extension` should inherit from
    ExtensionError
    """

    __TYPE = 'extension'

    def __init__(self, message, *args, extension: str='', **kwargs):
        super().__init__(message, *args, **kwargs)
        self.extension = extension
        self.attr_stack.append([self.__TYPE, {'extension': self.extension}])


class RendererError(ExtensionError):
    """The MFR related errors raised from a :class:`mfr.core.extension` and relating to rendering
    should inherit from RendererError
    """

    __TYPE = 'renderer'

    def __init__(self, message, *args, renderer_class: str='', **kwargs):
        super().__init__(message, *args, **kwargs)
        self.renderer_class = renderer_class
        self.attr_stack.append([self.__TYPE, {'class': self.renderer_class}])


class ExporterError(ExtensionError):
    """The MFR related errors raised from a :class:`mfr.core.extension` and relating to exporting
    should inherit from ExporterError
    """

    __TYPE = 'exporter'

    def __init__(self, message, *args, exporter_class: str='', **kwargs):
        super().__init__(message, *args, **kwargs)
        self.exporter_class = exporter_class
        self.attr_stack.append([self.__TYPE, {'exporter_class': self.exporter_class}])


class SubprocessError(ExporterError):
    """The MFR related errors raised from a :class:`mfr.core.extension` and relating to subprocess
    should inherit from SubprocessError
    """

    __TYPE = 'subprocess'

    def __init__(self, message, *args, code: int=500, process: str='', cmd: str='',
                 returncode: int=None, path: str='', **kwargs):
        super().__init__(message, *args, code=code, **kwargs)
        self.process = process
        self.cmd = cmd
        self.return_code = returncode
        self.path = path
        self.attr_stack.append([self.__TYPE, {
            'process': self.process,
            'cmd': self.cmd,
            'returncode': self.return_code,
            'path': self.path,
        }])


class ProviderError(PluginError):
    """The MFR related errors raised from a :class:`mfr.core.provider` should inherit from
    ProviderError
    """

    __TYPE = 'provider'

    def __init__(self, message, *args, provider: str='', **kwargs):
        super().__init__(message, *args, **kwargs)
        self.provider = provider
        self.attr_stack.append([self.__TYPE, {'provider': self.provider}])


class DownloadError(ProviderError):
    """The MFR related errors raised from a :class:`mfr.core.provider` and relating to downloads
    should inherit from DownloadError
    """

    __TYPE = 'download'

    def __init__(self, message, *args, download_url: str='', response: str='', **kwargs):
        super().__init__(message, *args, **kwargs)
        self.download_url = download_url
        self.response = response
        self.attr_stack.append([self.__TYPE, {
            'download_url': self.download_url,
            'response': self.response
        }])


class MetadataError(ProviderError):
    """The MFR related errors raised from a :class:`mfr.core.provider` and relating to metadata
    should inherit from MetadataError
    """

    __TYPE = 'metadata'

    def __init__(self, message, *args, metadata_url: str='', response: str='', **kwargs):
        super().__init__(message, *args, **kwargs)
        self.metadata_url = metadata_url
        self.response = response
        self.attr_stack.append([self.__TYPE, {
            'metadata_url': self.metadata_url,
            'response': self.response
        }])


class DriverManagerError(PluginError):

    __TYPE = 'drivermanager'

    def __init__(self, message, *args, namespace: str='', name: str='', invoke_on_load: bool=None,
                 invoke_args: dict=None, **kwargs):
        super().__init__(message, *args, **kwargs)

        self.namespace = namespace
        self.name = name
        self.invoke_on_load = invoke_on_load
        self.invoke_args = invoke_args or {}

        self.attr_stack.append([self.__TYPE, {
            'namespace': self.namespace,
            'name': self.name,
            'invoke_on_load': self.invoke_on_load,
            'invoke_args': self.invoke_args,
        }])


class MakeProviderError(DriverManagerError):
    """Thrown when MFR can't find an applicable provider class.  This indicates programmer error,
    so ``code`` defaults to ``500``."""

    def __init__(self, message, *args, code: int=500, **kwargs):
        super().__init__(message, *args, code=code, **kwargs)


class UnsupportedExtensionError(DriverManagerError):
    """When make_renderer and make_exporter fail, it's usually because MFR doesn't support that
    extension yet.  This error inherits from DriverManagerError (since it's the DriverManager that
    trips this) and includes a handler_type argsument
    """

    __TYPE = 'unsupported_extension'

    def __init__(self, *args, code: int=400, handler_type: str='', **kwargs):
        super().__init__(*args, code=code, **kwargs)

        self.handler_type = handler_type

        self.attr_stack.append([self.__TYPE, {'handler_type': self.handler_type}])


class MakeRendererError(UnsupportedExtensionError):
    """The MFR related errors raised from a :def:`mfr.core.utils.make_renderer` should inherit from
    MakeRendererError
    """

    def __init__(self, *args, **kwargs):
        super().__init__(settings.UNSUPPORTED_RENDER_MSG, *args, handler_type='renderer',
                         **kwargs)


class MakeExporterError(UnsupportedExtensionError):
    """The MFR related errors raised from a :def:`mfr.core.utils.make_exporter` should inherit from
    MakeExporterError
    """

    def __init__(self, *args, **kwargs):
        super().__init__(settings.UNSUPPORTED_EXPORTER_MSG, *args, handler_type='exporter',
                         **kwargs)
