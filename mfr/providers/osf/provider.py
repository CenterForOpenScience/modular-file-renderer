import os
import asyncio
import hashlib

import aiohttp

from mfr.core import exceptions
from mfr.core import provider
from mfr.core import streams


class OsfProvider(provider.BaseProvider):

    def __init__(self, request, url):
        super().__init__(request, url)
        self.download_url = None
        self.headers = {}

        # capture request authorization
        authorization = self.request.headers.get('Authorization')
        if authorization and authorization.startswith('Bearer '):
            self.headers['Authorization'] = authorization
        elif 'token' in self.request.arguments:
            self.headers['Authorization'] = 'Bearer ' + self.request.arguments['token'][0]

    @asyncio.coroutine
    def metadata(self):
        download_url = yield from self._fetch_download_url()
        metadata_url = download_url.replace('/file?', '/data?', 1)
        metadata_request = yield from self._make_request('GET', metadata_url)
        metadata = yield from metadata_request.json()
        # e.g.,
        # metadata = {'data': {
        #     'name': 'blah.pdf',
        #     'extra': {
        #         'revisionId': '1234',
        #     },
        # }}
        _, ext = os.path.splitext(metadata['data']['name'])
        # TODO: Add UniqueKey to WaterButler metadata, currently extra data varies per provider ('revisionId', 'version', etc)
        unique_key = u'{}+{}'.format(self.url, metadata['data']['extra']['version'])
        unique_key_hash = hashlib.sha256(unique_key.encode('utf-8')).hexdigest()
        return ext, unique_key_hash

    @asyncio.coroutine
    def download(self):
        download_url = yield from self._fetch_download_url()
        response = yield from self._make_request('GET', download_url)
        return streams.ResponseStreamReader(response)

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
        kwargs['headers'].update(self.headers)
        return (yield from aiohttp.request(method, url, *args, **kwargs))
