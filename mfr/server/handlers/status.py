import pkg_resources
import tornado.web

import mfr

class StatusHandler(tornado.web.RequestHandler):

    def get(self):
        """List information about modular-file-renderer status"""

        self.write({
            'status': 'up',
            'version': mfr.__version__,
        })
