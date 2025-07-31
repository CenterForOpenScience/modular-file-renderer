import asyncio
import logging
import signal
import time
from functools import partial

import sentry_sdk
import tornado.httpserver
import tornado.platform.asyncio
import tornado.web
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.tornado import TornadoIntegration

from mfr import settings
from mfr.server import settings as server_settings
from mfr.server.handlers.core import ExtensionsStaticFileHandler
from mfr.server.handlers.export import ExportHandler
from mfr.server.handlers.exporters import ExportersHandler
from mfr.server.handlers.render import RenderHandler
from mfr.server.handlers.renderers import RenderersHandler
from mfr.server.handlers.status import StatusHandler
from mfr.version import __version__

logger = logging.getLogger(__name__)
access_logger = logging.getLogger("tornado.access")


def sig_handler(sig, frame):
    """
    https://stackoverflow.com/questions/34554247/python-tornado-i-o-loop-current-vs-instance-method
    https://www.tornadoweb.org/en/branch6.3/_modules/tornado/testing.html
    """
    io_loop = tornado.ioloop.IOLoop.current()
    loop = io_loop.asyncio_loop  # Access the asyncio loop from Tornado

    def stop_loop():
        """
        Retrieve all tasks associated with tornado in asyncio loop
        Todo: (maybe there is more explicit way to check than 'tornado' in repr(task))
        """
        exists_tornado_task = any(
            task for task in asyncio.all_tasks(loop) if "tornado" in repr(task)
        )
        if exists_tornado_task:
            io_loop.call_later(1, stop_loop)
        else:
            io_loop.stop()

    io_loop.add_callback_from_signal(stop_loop)


def almost_apache_style_log(handler):
    """without status code and body length"""
    req = handler.request
    access_logger.info(
        '%s - - [%s +0800] "%s %s %s" - - "%s" "%s"'
        % (
            req.remote_ip,
            time.strftime("%d/%b/%Y:%X"),
            req.method,
            req.uri,
            req.version,
            getattr(req, "referer", "-"),
            req.headers["User-Agent"],
        )
    )


def make_app(debug):
    sentry_logging = LoggingIntegration(
        level=logging.INFO,  # Capture INFO level and above as breadcrumbs
        event_level=None,  # Do not send logs of any level as events
    )
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        release=__version__,
        integrations=[
            TornadoIntegration(),
            sentry_logging,
        ],
    )
    app = tornado.web.Application(
        [
            (
                r"/static/(.*)",
                tornado.web.StaticFileHandler,
                {"path": server_settings.STATIC_PATH},
            ),
            (r"/assets/(?P<module>[^/]+)/(?P<path>.*)", ExtensionsStaticFileHandler),
            (r"/export", ExportHandler),
            (r"/exporters", ExportersHandler),
            (r"/render", RenderHandler),
            (r"/renderers", RenderersHandler),
            (r"/status", StatusHandler),
        ],
        debug=debug,
        log_function=almost_apache_style_log,
    )
    return app


def serve():
    tornado.platform.asyncio.AsyncIOMainLoop().install()

    app = make_app(server_settings.DEBUG)

    ssl_options = None
    if server_settings.SSL_CERT_FILE and server_settings.SSL_KEY_FILE:
        ssl_options = {
            "certfile": server_settings.SSL_CERT_FILE,
            "keyfile": server_settings.SSL_KEY_FILE,
        }

    app.listen(
        server_settings.PORT,
        address=server_settings.ADDRESS,
        xheaders=server_settings.XHEADERS,
        max_buffer_size=server_settings.MAX_BUFFER_SIZE,
        ssl_options=ssl_options,
    )

    logger.info(f"Listening on {server_settings.ADDRESS}:{server_settings.PORT}")

    signal.signal(signal.SIGTERM, partial(sig_handler))
    asyncio.get_event_loop().set_debug(server_settings.DEBUG)
    asyncio.get_event_loop().run_forever()
