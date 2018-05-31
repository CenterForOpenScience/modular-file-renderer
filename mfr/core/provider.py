import abc
import markupsafe

import furl

from mfr.core import exceptions
from mfr.server import settings
from mfr.core.metrics import MetricsRecord


class BaseProvider(metaclass=abc.ABCMeta):
    """Base class for MFR Providers.  Requires ``download`` and ``metadata`` methods.
    Validates that the given file url is hosted at a domain listed in
    `mfr.server.settings.ALLOWED_PROVIDER_DOMAINS`.
    """

    def __init__(self, request, url, action=None):
        self.request = request
        url_netloc = furl.furl(url).netloc
        if url_netloc not in settings.ALLOWED_PROVIDER_NETLOCS:
            raise exceptions.ProviderError(
                message="{} is not a permitted provider domain.".format(
                    markupsafe.escape(url_netloc)
                ),
                code=400
            )
        self.url = url
        self.action = action
        self.provider_metrics = MetricsRecord('provider')
        self.metrics = self.provider_metrics.new_subrecord(self.NAME)

        self.provider_metrics.merge({
            'type': self.NAME,
            'url': str(self.url),
        })

    @abc.abstractproperty
    def NAME(self):
        raise NotImplementedError

    @abc.abstractmethod
    def metadata(self):
        pass

    @abc.abstractmethod
    def download(self):
        pass


class ProviderMetadata:

    def __init__(self, name, ext, content_type, unique_key, download_url, stable_id=None):
        self.name = name
        self.ext = ext
        self.content_type = content_type
        self.unique_key = unique_key
        self.download_url = download_url
        self.stable_id = stable_id

    def serialize(self):
        return {
            'name': self.name,
            'ext': self.ext,
            'content_type': self.content_type,
            'unique_key': str(self.unique_key),
            'download_url': str(self.download_url),
            'stable_id': None if self.stable_id is None else str(self.stable_id),
        }
