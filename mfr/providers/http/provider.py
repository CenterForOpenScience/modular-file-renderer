import os
import asyncio
import hashlib
import mimetypes
from urllib.parse import urlparse

import aiohttp

from waterbutler.core import streams

from mfr.core import provider
from mfr.core import exceptions


class HttpProvider(provider.BaseProvider):

    @asyncio.coroutine
    def metadata(self):
        path = urlparse(self.url).path
        name, ext = os.path.splitext(os.path.split(path)[-1])
        content_type, _ = mimetypes.guess_type(self.url)
        unique_key = hashlib.sha256(self.url.encode('utf-8')).hexdigest()
        return provider.ProviderMetadata(name, ext, content_type, unique_key, self.url)

    @asyncio.coroutine
    def download(self):
        response = yield from aiohttp.request('GET', self.url)
        if response.status >= 400:
            raise exceptions.ProviderError('Unable to download the requested file, please try again later.', code=response.status)
        return streams.ResponseStreamReader(response)
