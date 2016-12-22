import asyncio

import tornado.web
import tornado.httpserver
import tornado.platform.asyncio
import logging

from raven.contrib.tornado import AsyncSentryClient

import mfr
from mfr import settings
from mfr.server import settings as server_settings
from mfr.server.handlers.export import ExportHandler
from mfr.server.handlers.render import RenderHandler
from mfr.server.handlers.status import StatusHandler
from mfr.server.handlers.core import ExtensionsStaticFileHandler
from mfr.core import remote_logging

logger = logging.getLogger(__name__)

if server_settings.KEEN_PRIVATE_PROJECT_ID is None:
    logger.info('No KEEN_PRIVATE_PROJECT_ID configured. Exceptions will not be logged to keen.io')
else:
    keen_err_logger = logging.getLogger('keen_err_logger')
    keen_err_handler = remote_logging.KeenHandler('mfr_errors',
                                    server_settings.KEEN_PRIVATE_PROJECT_ID,
                                    server_settings.KEEN_PRIVATE_WRITE_KEY)
    keen_err_logger.addHandler(keen_err_handler)


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
    app.sentry_client = AsyncSentryClient(settings.SENTRY_DSN, release=mfr.__version__)
    return app


def serve():
    tornado.platform.asyncio.AsyncIOMainLoop().install()

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
