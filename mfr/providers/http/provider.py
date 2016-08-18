import os
import hashlib
import logging
import mimetypes
from urllib.parse import urlparse

import aiohttp

from waterbutler.core import streams

from mfr.core import provider
from mfr.core import exceptions

logger = logging.getLogger(__name__)


class HttpProvider(provider.BaseProvider):
    """Basic MFR provider.  Infers file metadata (extension, type) from the url. Downloads by
    issuing a GET to the url.
    """

    async def metadata(self):
        path = urlparse(self.url).path
        name, ext = os.path.splitext(os.path.split(path)[-1])
        content_type, _ = mimetypes.guess_type(self.url)
        unique_key = hashlib.sha256(self.url.encode('utf-8')).hexdigest()
        return provider.ProviderMetadata(name, ext, content_type, unique_key, self.url)

    async def download(self):
        response = await aiohttp.request('GET', self.url)
        if response.status >= 400:
            err_resp = await response.read()
            logger.error('Unable to download file: ({}) {}'.format(response.status, err_resp.decode('utf-8')))
            raise exceptions.ProviderError(
                'Unable to download the requested file, please try again later.',
                code=response.status
            )
        return streams.ResponseStreamReader(response)
