import gc
import asyncio

import tornado.web
import tornado.httpserver
import tornado.platform.asyncio
import logging

from mfr import settings
from mfr.core.utils import AioSentryClient
from mfr.server import settings as server_settings
from mfr.server.handlers.export import ExportHandler
from mfr.server.handlers.render import RenderHandler
from mfr.server.handlers.status import StatusHandler
from mfr.server.handlers.core import ExtensionsStaticFileHandler

logger = logging.getLogger(__name__)


def make_app(debug):
    app = tornado.web.Application(
        [
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': server_settings.STATIC_PATH}),
            (r'/assets/(.*?)/(.*\..*)', ExtensionsStaticFileHandler),
            (r'/export', ExportHandler),
            (r'/render', RenderHandler),
            (r'/status', StatusHandler),
        ],
        debug=debug,
    )
    # Fix package import
    app.sentry_client = AioSentryClient(settings.get('SENTRY_DSN', None))
    return app


@asyncio.coroutine
def cleanup():
    # Forces exceptions to be garbage collected
    # This is fixed in python 3.5 but needs manual collection in 3.4
    while True:
        gc.collect()
        yield from asyncio.sleep(1)


def serve():
    tornado.platform.asyncio.AsyncIOMainLoop().install()

    asyncio.async(cleanup())

    app = make_app(server_settings.DEBUG)

    ssl_options = None
    if server_settings.SSL_CERT_FILE and server_settings.SSL_KEY_FILE:
        ssl_options = {
            'certfile': server_settings.SSL_CERT_FILE,
            'keyfile': server_settings.SSL_KEY_FILE,
        }

    app.listen(
        server_settings.PORT,
        address=server_settings.ADDRESS,
        xheaders=server_settings.XHEADERS,
        max_buffer_size=server_settings.MAX_BUFFER_SIZE,
        ssl_options=ssl_options,
    )

    logger.info("Listening on {0}:{1}".format(server_settings.ADDRESS, server_settings.PORT))

    asyncio.get_event_loop().set_debug(server_settings.DEBUG)
    asyncio.get_event_loop().run_forever()
