import os
import asyncio
import hashlib
import mimetypes
from urllib.parse import urlparse

import aiohttp

from waterbutler.core import streams

from mfr.core import provider


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
        return streams.ResponseStreamReader(response)
