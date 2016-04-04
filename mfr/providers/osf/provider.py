import os
import json
import hashlib
import logging
import mimetypes

import furl
import aiohttp

from waterbutler.core import streams

from mfr.core import exceptions
from mfr.core import provider

logger = logging.getLogger(__name__)


class OsfProvider(provider.BaseProvider):

    UNNEEDED_URL_PARAMS = ('_', 'token', 'action', 'mode', 'displayName')

    def __init__(self, request, url):
        super().__init__(request, url)
        self.download_url = None
        self.headers = {}

        # capture request authorization
        self.cookies = dict(self.request.cookies)
        self.cookie = self.request.query_arguments.get('cookie')
        self.view_only = self.request.query_arguments.get('view_only')
        self.authorization = self.request.headers.get('Authorization')
        if self.cookie:
            self.cookie = self.cookie[0].decode()
        if self.view_only:
            self.view_only = self.view_only[0].decode()

    async def metadata(self):
        download_url = await self._fetch_download_url()
        if '/file?' in download_url:
            # TODO Remove this when API v0 is officially deprecated
            metadata_url = download_url.replace('/file?', '/data?', 1)
            metadata_request = await self._make_request('GET', metadata_url)
            metadata = await metadata_request.json()
        else:
            metadata_request = await self._make_request('HEAD', download_url)
            # To make changes to current code as minimal as possible
            metadata = {'data': json.loads(metadata_request.headers['x-waterbutler-metadata'])['attributes']}
        await metadata_request.release()

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

    async def download(self):
        download_url = await self._fetch_download_url()
        response = await self._make_request('GET', download_url, allow_redirects=False)

        if response.status >= 400:
            err_resp = await response.read()
            logger.error('Unable to download file: ({}) {}'.format(response.status, err_resp.decode('utf-8')))
            raise exceptions.ProviderError(
                'Unable to download the requested file, please try again later.',
                code=response.status
            )

        if response.status in (302, 301):
            await response.release()
            response = await aiohttp.request('GET', response.headers['location'])

        return streams.ResponseStreamReader(response, unsizable=True)

    async def _fetch_download_url(self):
        if not self.download_url:
            # make request to osf, don't follow, store waterbutler download url
            request = await self._make_request(
                'GET',
                self.url,
                allow_redirects=False,
                headers={
                    'Content-Type': 'application/json'
                }
            )
            await request.release()

            if request.status != 302:
                raise exceptions.ProviderError(request.reason, request.status)
            self.download_url = request.headers['location']
        return self.download_url

    async def _make_request(self, method, url, *args, **kwargs):
        if self.cookies:
            kwargs['cookies'] = self.cookies
        if self.cookie:
            kwargs.setdefault('params', {})['cookie'] = self.cookie
        if self.view_only:
            kwargs.setdefault('params', {})['view_only'] = self.view_only
        if self.authorization:
            kwargs.setdefault('headers', {})['Authorization'] = 'Bearer ' + self.token

        return (await aiohttp.request(method, url, *args, **kwargs))
