import os
import asyncio
import pkg_resources

import tornado.web
from raven.contrib.tornado import SentryMixin

import waterbutler.core.utils
import waterbutler.server.utils
import waterbutler.core.exceptions

from mfr.core import utils
from mfr.server import settings
from mfr.core import exceptions


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


class CorsMixin(tornado.web.RequestHandler):

    def set_default_headers(self):
        if isinstance(settings.CORS_ALLOW_ORIGIN, str):
            self.set_header('Access-Control-Allow-Origin', settings.CORS_ALLOW_ORIGIN)
        else:
            if self.request.headers.get('Origin') in settings.CORS_ALLOW_ORIGIN:
                self.set_header('Access-Control-Allow-Origin', self.request.headers['Origin'])
        self.set_header('Access-Control-Allow-Headers', ', '.join(CORS_ACCEPT_HEADERS))
        self.set_header('Access-Control-Expose-Headers', ', '.join(CORS_EXPOSE_HEADERS))
        self.set_header('Cache-control', 'no-store, no-cache, must-revalidate, max-age=0')

    def options(self):
        self.set_status(204)
        self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE'),


class BaseHandler(CorsMixin, tornado.web.RequestHandler, SentryMixin):

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

        self.ext, self.unique_key, self.download_url = yield from self.provider.metadata()

        self.cache_provider = waterbutler.core.utils.make_provider(
            settings.CACHE_PROVIDER_NAME,
            {},  # User information which can be left blank
            settings.CACHE_PROVIDER_CREDENTIALS,
            settings.CACHE_PROVIDER_SETTINGS
        )

        self.local_cache_provider = waterbutler.core.utils.make_provider(
            'filesystem', {}, {}, settings.LOCAL_CACHE_PROVIDER_SETTINGS
        )

    @asyncio.coroutine
    def write_stream(self, stream):
        while True:
            chunk = yield from stream.read(settings.CHUNK_SIZE)
            if not chunk:
                break
            self.write(chunk)
            yield from waterbutler.server.utils.future_wrapper(self.flush())

    def write_error(self, status_code, exc_info):
        self.captureException(exc_info)  # Log all non 2XX codes to sentry
        etype, exc, _ = exc_info

        if issubclass(etype, exceptions.PluginError):
            self.set_status(exc.code)
            self.finish(exc.as_html())
        else:
            self.set_status(400)
            self.finish('''
                <link rel="stylesheet" href="/static/css/bootstrap.min.css">
                <div class="alert alert-warning" role="alert">
                    Unable to render the requested file, please try again later.
                </div>
            ''')


class ExtensionsStaticFileHandler(tornado.web.StaticFileHandler, CorsMixin):
    """Extensions static path definitions
    """

    def initialize(self):
        namespace = 'mfr.renderers'
        module_path = 'mfr.extensions'
        self.modules = {
            ep.module_name.replace(module_path + '.', ''): os.path.join(ep.dist.location, 'mfr', 'extensions', ep.module_name.replace(module_path + '.', ''), 'static')
            for ep in list(pkg_resources.iter_entry_points(namespace))
        }

    @waterbutler.server.utils.coroutine
    def get(self, module_name, path):
        try:
            super().initialize(self.modules[module_name])
            return (yield from waterbutler.server.utils.future_wrapper(super().get(path)))
        except Exception:
            self.set_status(404)

        try:
            super().initialize(settings.STATIC_PATH)
            return (yield from waterbutler.server.utils.future_wrapper(super().get(path)))
        except Exception:
            self.set_status(404)
