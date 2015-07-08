import os
import asyncio
import hashlib
import mimetypes

import furl
import aiohttp

from waterbutler.core import streams

from mfr.core import exceptions
from mfr.core import provider


class OsfProvider(provider.BaseProvider):

    UNNEEDED_URL_PARAMS = ('_', 'token', 'action', 'mode', 'displayName')

    def __init__(self, request, url):
        super().__init__(request, url)
        self.download_url = None
        self.headers = {}

        # capture request authorization
        authorization = self.request.headers.get('Authorization')
        if authorization and authorization.startswith('Bearer '):
            self.token = authorization[7:].decode('utf')
        elif 'token' in self.request.arguments:
            self.token = self.request.arguments['token'][0].decode('utf-8')
        else:
            self.token = None

    @asyncio.coroutine
    def metadata(self):
        download_url = yield from self._fetch_download_url()
        metadata_url = download_url.replace('/file?', '/data?', 1)
        metadata_request = yield from self._make_request('GET', metadata_url)
        metadata = yield from metadata_request.json()
        # e.g.,
        # metadata = {'data': {
        #     'name': 'blah.png',
        #     'contentType': 'image/png',
        #     'etag': 'ABCD123456...',
        #     'extra': {
        #         ...
        #     },
        # }}
        name, ext = os.path.splitext(metadata['data']['name'])
        content_type = metadata['data']['contentType'] or mimetypes.guess_type(metadata['data']['name'])[0]
        cleaned_url = furl.furl(download_url)
        for unneeded in OsfProvider.UNNEEDED_URL_PARAMS:
            cleaned_url.args.pop(unneeded, None)
        unique_key = hashlib.sha256((metadata['data']['etag'] + cleaned_url.url).encode('utf-8')).hexdigest()
        return provider.ProviderMetadata(name, ext, content_type, unique_key, download_url)

    @asyncio.coroutine
    def download(self):
        download_url = yield from self._fetch_download_url()
        response = yield from self._make_request('GET', download_url, allow_redirects=False)
        if response.status >= 400:
            raise exceptions.ProviderError('Unable to download the requested file, please try again later.', code=response.status)
        if response.status in (302, 301):
            response = yield from aiohttp.request('GET', response.headers['location'])
        download_stream = streams.ResponseStreamReader(response, unsizable=True)
        download_stream.add_writer('md5', streams.HashStreamWriter(hashlib.md5))
        return download_stream

    @asyncio.coroutine
    def _fetch_download_url(self):
        if not self.download_url:
            # make request to osf, don't follow, store waterbutler download url
            request = yield from self._make_request(
                'GET',
                self.url,
                allow_redirects=False,
                headers={
                    'Content-Type': 'application/json'
                }
            )
            if request.status != 302:
                raise exceptions.ProviderError(request.reason, request.status)
            self.download_url = request.headers['location']
        return self.download_url

    @asyncio.coroutine
    def _make_request(self, method, url, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        if self.token:
            kwargs['headers']['Authorization'] = 'Bearer ' + self.token
        return (yield from aiohttp.request(method, url, *args, **kwargs))
