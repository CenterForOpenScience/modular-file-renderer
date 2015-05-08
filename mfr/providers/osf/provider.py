import os
import http
import json
import asyncio
import hashlib

import aiohttp

# from waterbutler.core import utils
# from waterbutler.core import streams
from mfr.core import provider
# from waterbutler.core import exceptions
#
from mfr.providers.osf import settings


class OsfProvider(provider.BaseProvider):

    @asyncio.coroutine
    def metadata(self):
        # make request to osf, don't follow, for waterbutler url
        # modify url for metadata

        # TODO: Add Auth Token
        request = yield from aiohttp.request('GET', self.url, allow_redirects=False)
        metadata_url = request.headers['location'].replace('/file?', '/data?', 1)

        metadata_request = yield from aiohttp.request('GET', metadata_url)
        metadata = yield from metadata_request.json()
        # metadata = {
        #     'name': 'blah.pdf',
        #     'extra': {
        #         'revisionId': '1234',
        #     },
        # }
        _, ext_name = os.path.splitext(metadata['data']['name'])
        # TODO: Add UniqueKey to WaterButler metadata, currently extra data varies per provider ('revisionId', 'version', etc)
        unique_key = u'{}+{}'.format(self.url, metadata['data']['extra']['version'])
        unique_key_hash = hashlib.sha256(unique_key.encode('utf-8')).hexdigest()
        return ext_name, unique_key_hash


    @asyncio.coroutine
    def download(self):
        # go to osf url
        # don't follow
        # get waterbutler url

        from mfr.core.streams import FileStreamReader

        file_pointer = open('/Users/michael/Downloads/cas_proxy_protocol.pdf', 'rb')
        return FileStreamReader(file_pointer)
