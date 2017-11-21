import tornado.web

from version import __version__


class StatusHandler(tornado.web.RequestHandler):

    def get(self):
        """List information about modular-file-renderer status"""
        self.write({
            'status': 'up',
            'version': __version__
        })
