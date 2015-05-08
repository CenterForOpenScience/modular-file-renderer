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
            self.url,
        )

        self.ext_name, self.unique_key = yield from self.provider.metadata()

    # def write_error(self, status_code, exc_info):
    #     self.captureException(exc_info)
    #     etype, exc, _ = exc_info
    #
    #     if issubclass(etype, exceptions.ProviderError):
    #         self.set_status(exc.code)
    #         if exc.data:
    #             self.finish(exc.data)
    #         else:
    #             self.finish({
    #                 'code': exc.code,
    #                 'message': exc.message
    #             })
    #     else:
    #         self.finish({
    #             'code': status_code,
    #             'message': self._reason,
    #         })
    #
    # def set_status(self, code, reason=None):
    #     return super().set_status(code, reason or HTTP_REASONS.get(code))
    #
    # def options(self):
    #     self.set_status(204)
    #     self.set_header('Access-Control-Allow-Methods', 'PUT, DELETE'),

    # @utils.async_retry(retries=5, backoff=5)
    # def _send_hook(self, action, metadata):
    #     payload = {
    #         'action': action,
    #         'provider': self.arguments['provider'],
    #         'metadata': metadata,
    #         'auth': self.payload['auth'],
    #         'time': time.time() + 60
    #     }
    #     message, signature = signer.sign_payload(payload)
    #     resp = aiohttp.request(
    #         'PUT',
    #         self.payload['callback_url'],
    #         data=json.dumps({
    #             'payload': message.decode(),
    #             'signature': signature,
    #         }),
    #         headers={'Content-Type': 'application/json'},
    #     )
    #     return resp


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
