import os
import asyncio
import hashlib

import aiohttp

from mfr.core import provider
from mfr.core import streams


class OsfProvider(provider.BaseProvider):

    def __init__(self, url):
        super().__init__(url)
        self._download_url = None

    @asyncio.coroutine
    def metadata(self):
        download_url = yield from self._fetch_download_url()
        metadata_url = download_url.replace('/file?', '/data?', 1)
        metadata_request = yield from aiohttp.request('GET', metadata_url)
        metadata = yield from metadata_request.json()
        # e.g.,
        # metadata = {'data': {
        #     'name': 'blah.pdf',
        #     'extra': {
        #         'revisionId': '1234',
        #     },
        # }}
        _, ext_name = os.path.splitext(metadata['data']['name'])
        # TODO: Add UniqueKey to WaterButler metadata, currently extra data varies per provider ('revisionId', 'version', etc)
        unique_key = u'{}+{}'.format(self.url, metadata['data']['extra']['version'])
        unique_key_hash = hashlib.sha256(unique_key.encode('utf-8')).hexdigest()
        return ext_name, unique_key_hash

    @asyncio.coroutine
    def download(self):
        download_url = yield from self._fetch_download_url()
        response = yield from aiohttp.request('GET', download_url)
        return streams.ResponseStreamReader(response)

    @asyncio.coroutine
    def _fetch_download_url(self):
        if not self._download_url:
            # TODO: Add auth token to header
            # make request to osf, don't follow, store waterbutler url
            request = yield from aiohttp.request('GET', self.url, allow_redirects=False)
            self._download_url = request.headers['location']
        return self._download_url
