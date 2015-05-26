import os
import asyncio
import pkg_resources

import tornado.web
from raven.contrib.tornado import SentryMixin

from mfr.core import utils
from mfr.server import settings


CORS_ACCEPT_HEADERS = [
    'Range',
    'Content-Type',
    'Cache-Control',
    'X-Requested-With',
]

CORS_EXPOSE_HEADERS = [
    'Accept-Ranges',
    'Content-Range',
    'Content-Length',
    'Content-Encoding',
]


class BaseHandler(tornado.web.RequestHandler, SentryMixin):

    ACTION_MAP = {}

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', settings.CORS_ALLOW_ORIGIN)
        self.set_header('Access-Control-Allow-Headers', ', '.join(CORS_ACCEPT_HEADERS))
        self.set_header('Access-Control-Expose-Headers', ', '.join(CORS_EXPOSE_HEADERS))
        self.set_header('Cache-control', 'no-store, no-cache, must-revalidate, max-age=0')

    @asyncio.coroutine
    def prepare(self):
        self.url = self.request.query_arguments['url'][0].decode('utf-8')

        self.provider = utils.make_provider(
            settings.PROVIDER_NAME,
            self.request,
            self.url
        )

        self.ext, self.unique_key = yield from self.provider.metadata()


class ExtensionsStaticFileHandler(tornado.web.StaticFileHandler):
    """Extensions static path definitions
    """

    def initialize(self):
        namespace = 'mfr.extensions'
        self.modules = {
            ep.module_name.replace(namespace + '.', ''): os.path.join(ep.dist.location, 'mfr', 'extensions', ep.module_name.replace(namespace + '.', ''), 'static')
            for ep in list(pkg_resources.iter_entry_points(namespace))
        }

    def set_extra_headers(self, path):
        self.set_header('Access-Control-Allow-Origin', settings.CORS_ALLOW_ORIGIN)
        self.set_header('Access-Control-Allow-Headers', ', '.join(CORS_ACCEPT_HEADERS))
        self.set_header('Access-Control-Expose-Headers', ', '.join(CORS_EXPOSE_HEADERS))
        self.set_header('Cache-control', 'no-store, no-cache, must-revalidate, max-age=0')

    def get(self, module_name, path):
        try:
            super().initialize(self.modules[module_name])
            return super().get(path).result()
        except Exception:
            self.set_status(404)
