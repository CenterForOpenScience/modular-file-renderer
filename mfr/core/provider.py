from abc import (
    ABCMeta,
    abstractmethod,
    abstractproperty
)

from aiohttp import HttpBadRequest
from furl import furl
import markupsafe

from mfr.core.exceptions import ProviderError
from mfr.core.metrics import MetricsRecord
from mfr.server.settings import ALLOWED_PROVIDER_NETLOCS


class BaseProvider(metaclass=ABCMeta):
    """Base class for MFR Providers.  Requires ``download`` and ``metadata`` methods.
    Validates that the given file url is hosted at a domain listed in
    `mfr.server.settings.ALLOWED_PROVIDER_DOMAINS`.
    """

    def __init__(self, request, url, action=None):
        self.request = request
        netloc = furl(url).netloc
        if netloc not in ALLOWED_PROVIDER_NETLOCS:
            raise ProviderError(
                message="{} is not a permitted provider domain.".format(
                    markupsafe.escape(netloc)
                ),
                # TODO: using HTTPStatus.BAD_REQUEST fails tests, not sure why and I will take a another look later
                code=HttpBadRequest.code
            )
        self.url = url
        self.action = action
        self.provider_metrics = MetricsRecord('provider')
        self.metrics = self.provider_metrics.new_subrecord(self.NAME)

        self.provider_metrics.merge({
            'type': self.NAME,
            'url': str(self.url),
        })

    @abstractproperty
    def NAME(self):
        raise NotImplementedError

    @abstractmethod
    def metadata(self):
        pass

    @abstractmethod
    def download(self):
        pass


class ProviderMetadata:

    def __init__(self, name, ext, content_type, unique_key,
                 download_url, is_public=False, stable_id=None):
        self.name = name
        self.ext = ext
        self.content_type = content_type
        self.unique_key = unique_key
        self.download_url = download_url
        self.stable_id = stable_id
        self.is_public = is_public

    def serialize(self):
        return {
            'name': self.name,
            'ext': self.ext,
            'content_type': self.content_type,
            'unique_key': str(self.unique_key),
            'download_url': str(self.download_url),
            'stable_id': None if self.stable_id is None else str(self.stable_id),
            'is_public': self.is_public,
        }
