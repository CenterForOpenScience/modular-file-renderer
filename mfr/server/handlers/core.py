import os
import asyncio
import pkg_resources

import tornado.web
import waterbutler.core.utils
from raven.contrib.tornado import SentryMixin

from mfr.core import utils
from mfr.server import settings
from mfr.server import exceptions


CORS_ACCEPT_HEADERS = [
    'Range',
    'Content-Type',
    'Authorization',
    'Cache-Control',
    'X-Requested-With',
]

CORS_EXPOSE_HEADERS = [
    'Accept-Ranges',
    'Content-Range',
    'Content-Length',
    'Content-Encoding',
]


class CorsMixin:

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', settings.CORS_ALLOW_ORIGIN)
        self.set_header('Access-Control-Allow-Headers', ', '.join(CORS_ACCEPT_HEADERS))
        self.set_header('Access-Control-Expose-Headers', ', '.join(CORS_EXPOSE_HEADERS))
        self.set_header('Cache-control', 'no-store, no-cache, must-revalidate, max-age=0')

    def options(self):
        self.set_status(204)
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE'),


class BaseHandler(CorsMixin, tornado.web.RequestHandler, SentryMixin):
    ACTION_MAP = {}

    @asyncio.coroutine
    def prepare(self):
        if self.request.method == 'OPTIONS':
            return

        self.url = self.request.query_arguments['url'][0].decode('utf-8')

        self.provider = utils.make_provider(
            settings.PROVIDER_NAME,
            self.request,
            self.url
        )

        self.ext, self.unique_key = yield from self.provider.metadata()

        self.cache_provider = waterbutler.core.utils.make_provider(
            settings.CACHE_PROVIDER_NAME,
            {},  # User information which can be left blank
            settings.CACHE_PROVIDER_CREDENTIALS,
            settings.CACHE_PROVIDER_SETTINGS
        )

        self.local_cache_provider = waterbutler.core.utils.make_provider('filesystem', {}, {}, {'folder': '/tmp/mfrlocalcache/'})

        self.unique_path = yield from self.cache_provider.validate_path('/' + self.unique_key)
        self.local_cache_path = yield from self.local_cache_provider.validate_path('/' + self.unique_key)

    def write_error(self, status_code, exc_info):
        self.captureException(exc_info)  # Log all non 2XX codes to sentry
        etype, exc, _ = exc_info

        if issubclass(etype, exceptions.MFRHTTPError):
            self.set_status(exc.status_code)
            self.finish(exc.as_html())
        else:
            super().write_error(status_code)


class ExtensionsStaticFileHandler(tornado.web.StaticFileHandler, CorsMixin):
    """Extensions static path definitions
    """

    def initialize(self):
        namespace = 'mfr.extensions'
        self.modules = {
            ep.module_name.replace(namespace + '.', ''): os.path.join(ep.dist.location, 'mfr', 'extensions', ep.module_name.replace(namespace + '.', ''), 'static')
            for ep in list(pkg_resources.iter_entry_points(namespace))
        }

    def get(self, module_name, path):
        try:
            super().initialize(self.modules[module_name])
            return super().get(path).result()
        except Exception:
            self.set_status(404)
