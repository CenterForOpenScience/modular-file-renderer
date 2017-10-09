import signal
import asyncio
from functools import partial

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

logger = logging.getLogger(__name__)


def sig_handler(sig, frame):
    io_loop = tornado.ioloop.IOLoop.instance()

    def stop_loop():
        if len(asyncio.Task.all_tasks(io_loop)) == 0:
            io_loop.stop()
        else:
            io_loop.call_later(1, stop_loop)

    io_loop.add_callback_from_signal(stop_loop)

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

    signal.signal(signal.SIGTERM, partial(sig_handler))
    asyncio.get_event_loop().set_debug(server_settings.DEBUG)
    asyncio.get_event_loop().run_forever()
