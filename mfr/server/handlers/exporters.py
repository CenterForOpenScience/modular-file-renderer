import pkg_resources
import tornado.web

class ExportersHandler(tornado.web.RequestHandler):

    def get(self):
        """List available exporters"""

        exporters = {}
        for ep in pkg_resources.iter_entry_points(group='mfr.exporters'):
            exporters.update({ep.name: ep.load().__name__})

        self.write({
            'exporters': exporters,
        })