import os
import abc
import uuid
import asyncio
import logging
import pkg_resources

import tornado.web
import tornado.iostream
from raven.contrib.tornado import SentryMixin

import waterbutler.core.utils
import waterbutler.server.utils
import waterbutler.core.exceptions

from mfr.server import settings
from mfr.core.metrics import MetricsRecord
from mfr.core import utils, exceptions, remote_logging

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

logger = logging.getLogger(__name__)


class CorsMixin:

    def _cross_origin_is_allowed(self):
        if self.request.method == 'OPTIONS':
            return True
        elif not self.request.cookies and self.request.headers.get('Authorization'):
            return True
        return False

    def set_default_headers(self):
        if not self.request.headers.get('Origin'):
            return

        allowed_origin = None
        if self._cross_origin_is_allowed():
            allowed_origin = self.request.headers['Origin']
        elif isinstance(settings.CORS_ALLOW_ORIGIN, str):
            if settings.CORS_ALLOW_ORIGIN == '*':
                # Wild cards cannot be used with allowCredentials.
                # Match Origin if its specified, makes pdfs and pdbs render properly
                allowed_origin = self.request.headers['Origin']
            else:
                allowed_origin = settings.CORS_ALLOW_ORIGIN
        else:
            if self.request.headers['Origin'] in settings.CORS_ALLOW_ORIGIN:
                allowed_origin = self.request.headers['Origin']

        if allowed_origin is not None:
            self.set_header('Access-Control-Allow-Origin', allowed_origin)

        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Headers', ', '.join(CORS_ACCEPT_HEADERS))
        self.set_header('Access-Control-Expose-Headers', ', '.join(CORS_EXPOSE_HEADERS))
        self.set_header('Cache-control', 'no-store, no-cache, must-revalidate, max-age=0')

    def options(self):
        self.set_status(204)
        if self.request.headers.get('Origin'):
            self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE'),


class BaseHandler(CorsMixin, tornado.web.RequestHandler, SentryMixin):
    """Base class for the Render and Export handlers.  Fetches the file metadata for the file
    indicated by the ``url`` query parameter and builds the provider caches.  Also handles
    writing output and errors.
    """

    bytes_written = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler_metrics = MetricsRecord('handler')
        self.handler_metrics.add('cache_file.result', None)
        self.handler_metrics.add('source_file.upload.required', True)

        self.metrics = self.handler_metrics.new_subrecord(self.NAME)

        self.extension_metrics = MetricsRecord('extension')

    @abc.abstractproperty
    def NAME(self):
        raise NotImplementedError

    async def prepare(self):
        """Builds an MFR provider instance, to which it passes the the ``url`` query parameter.
        From that, the file metadata is extracted.  Also builds cached waterbutler providers.
        """
        if self.request.method == 'OPTIONS':
            return

        try:
            self.url = self.request.query_arguments['url'][0].decode('utf-8')
        except KeyError:
            raise exceptions.ProviderError(
                '"url" is a required argument.',
                provider=settings.PROVIDER_NAME,
                code=400,
            )
        logging.debug('target_url::{}'.format(self.url))

        self.provider = utils.make_provider(
            settings.PROVIDER_NAME,
            self.request,
            self.url,
            action=self.NAME,
        )

        self.metadata = await self.provider.metadata()
        self.extension_metrics.add('ext', self.metadata.ext)
        logging.debug('extension::{}'.format(self.metadata.ext))

        self.cache_provider = waterbutler.core.utils.make_provider(
            settings.CACHE_PROVIDER_NAME,
            {},  # User information which can be left blank
            settings.CACHE_PROVIDER_CREDENTIALS,
            settings.CACHE_PROVIDER_SETTINGS
        )

        self.local_cache_provider = waterbutler.core.utils.make_provider(
            'filesystem', {}, {}, settings.LOCAL_CACHE_PROVIDER_SETTINGS
        )

        self.source_file_id = uuid.uuid4()
        self.add_header('X-MFR-REQUEST-ID', str(uuid.uuid4()))

    async def write_stream(self, stream):
        try:
            while True:
                chunk = await stream.read(settings.CHUNK_SIZE)
                if not chunk:
                    break
                # Temp fix, write does not accept bytearrays currently
                if isinstance(chunk, bytearray):
                    chunk = bytes(chunk)
                self.bytes_written += len(chunk)
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
            try:  # clever errors shouldn't break other things
                current, child_type = {}, None
                for level in reversed(exc.attr_stack):
                    if current:
                        current = {'{}_{}'.format(level[0], child_type): current}
                        current['child_type'] = child_type
                    current.update(level[1])
                    current['self_type'] = level[0]
                    child_type = level[0]

                current['materialized_type'] = '.'.join([x[0] for x in exc.attr_stack])
                self.error_metrics = current
            except Exception:
                pass
            self.set_status(exc.code)
            self.finish(exc.as_html())
        else:
            self.error_metrics = {
                'code': self.get_status(),
                'message': str(exc),
                'self_type': 'error',
                'child_type': 'nonspecific',
                'materialized_type': 'error.nonspecific',
                'error_nonspecific': {
                    'self_type': 'nonspecific',
                    'class': etype.__name__,
                    'data': repr(exc),
                },
            }
            self.set_status(400)
            self.finish('''
                <link rel="stylesheet" href="/static/css/bootstrap.min.css">
                <div class="alert alert-warning" role="alert">
                    Unable to render the requested file, please try again later.
                </div>
            ''')

    # avoid dumping duplicate information to application log
    def log_exception(self, typ, value, tb):
        if isinstance(value, tornado.web.HTTPError):
            if value.log_message:
                format = "%d %s: " + value.log_message
                args = ([value.status_code, self._request_summary()] +
                        list(value.args))
                tornado.web.gen_log.warning(format, *args)
        else:
            tornado.web.app_log.error("[User-Agent: %s] Uncaught exception %s\n",
                                      self.request.headers.get('User-Agent', '*none found*'),
                                      self._request_summary(),
                                      exc_info=(typ, value, tb))

    def on_finish(self):
        if self.request.method not in self.ALLOWED_METHODS:
            return

        self.handler_metrics.merge({
            'type': self.NAME,
            'bytes_written': self.bytes_written,
            # 'elpased': elapsed.serialize(),
            'cache_file': {
                'id': str(getattr(self, 'cache_file_id', '')),
                'path': str(getattr(self, 'cache_file_path', '')),
            },
            'source_file': {
                'id': str(getattr(self, 'source_file_id', '')),
                'path': str(getattr(self, 'source_file_path', '')),
            }
        })

        if hasattr(self, 'cache_provider'):
            self.handler_metrics.merge({
                'cache_file': {
                    'provider': self.cache_provider.NAME
                }
            })

        if hasattr(self, 'local_cache_provider'):
            self.handler_metrics.merge({
                'source_file': {
                    'provider': self.local_cache_provider.NAME
                }
            })

        asyncio.ensure_future(self._cache_and_clean())
        asyncio.ensure_future(
            remote_logging.log_analytics(
                remote_logging._serialize_request(self.request),
                self._all_metrics(), is_error=hasattr(self, 'error_metrics')))

    async def _cache_and_clean(self):
        return

    def _all_metrics(self):
        metrics = {
            'handler': self.handler_metrics.serialize(),
        }

        metrics_attrs = [
            ('extension', 'extension_metrics'),
            ('file', 'metadata'),
            ('renderer', 'renderer_metrics'),
            ('exporter', 'exporter_metrics'),
        ]
        for (key, name) in metrics_attrs:
            metrics[key] = getattr(self, name).serialize() if hasattr(self, name) else None

        if hasattr(self, 'provider') and hasattr(self.provider, 'provider_metrics'):
            metrics['provider'] = self.provider.provider_metrics.serialize()

        # error_metrics is already serialized
        metrics['error'] = getattr(self, 'error_metrics') if hasattr(self, 'error_metrics') else None
        return metrics


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
