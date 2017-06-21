import pkg_resources
import tornado.web

import mfr

class StatusHandler(tornado.web.RequestHandler):

    def get(self):
        """List information about modular-file-renderer status"""

        exporters = {}
        for ep in pkg_resources.iter_entry_points(group='mfr.exporters'):
            exporters.update({ep.name: ep.load().__name__})

        renderers = {}
        for ep in pkg_resources.iter_entry_points(group='mfr.renderers'):
            renderers.update({ep.name: ep.load().__name__})

        self.write({
            'status': 'up',
            'version': mfr.__version__,
            'exporters': exporters,
            'renderers': renderers,
        })
