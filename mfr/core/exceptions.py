import waterbutler.core.exceptions


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
    """
