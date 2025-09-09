import abc
from dataclasses import dataclass

import markupsafe

import furl

from mfr.core import exceptions
from mfr.server import settings
from mfr.core.metrics import MetricsRecord
from mfr.tasks.serializer import serializable


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

    @abc.abstractmethod
    def NAME(self):
        # Todo: not see Name implementation in child classes
        raise NotImplementedError

    @abc.abstractmethod
    def metadata(self):
        pass

    @abc.abstractmethod
    def download(self):
        pass

@serializable
@dataclass
class ProviderMetadata:
    name: str
    ext: str
    content_type: str
    unique_key: str
    download_url: str
    stable_id: str = None

    def serialize(self):
        return {
            'name': self.name,
            'ext': self.ext,
            'content_type': self.content_type,
            'unique_key': str(self.unique_key),
            'download_url': str(self.download_url),
            'stable_id': None if self.stable_id is None else str(self.stable_id),
        }
