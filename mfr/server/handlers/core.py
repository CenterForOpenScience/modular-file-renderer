import os
import pkg_resources

import tornado.web
import tornado.iostream
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

    async def prepare(self):
        if self.request.method == 'OPTIONS':
            return

        self.url = self.request.query_arguments['url'][0].decode('utf-8')

        self.provider = utils.make_provider(
            settings.PROVIDER_NAME,
            self.request,
            self.url
        )

        self.metadata = await self.provider.metadata()

        self.cache_provider = waterbutler.core.utils.make_provider(
            settings.CACHE_PROVIDER_NAME,
            {},  # User information which can be left blank
            settings.CACHE_PROVIDER_CREDENTIALS,
            settings.CACHE_PROVIDER_SETTINGS
        )

        self.local_cache_provider = waterbutler.core.utils.make_provider(
            'filesystem', {}, {}, settings.LOCAL_CACHE_PROVIDER_SETTINGS
        )

    async def write_stream(self, stream):
        try:
            while True:
                chunk = await stream.read(settings.CHUNK_SIZE)
                if not chunk:
                    break
                # Temp fix, write does not accept bytearrays currently
                if isinstance(chunk, bytearray):
                    chunk = bytes(chunk)
                self.write(chunk)
                del chunk
                await self.flush()
        except tornado.iostream.StreamClosedError:
            # Client has disconnected early.
            # No need for any exception to be raised
            return

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

    async def get(self, module_name, path):
        try:
            super().initialize(self.modules[module_name])
            return await super().get(path)
        except Exception:
            self.set_status(404)

        try:
            super().initialize(settings.STATIC_PATH)
            return await super().get(path)
        except Exception:
            self.set_status(404)
