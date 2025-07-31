from importlib.metadata import entry_points
import tornado.web


class ExportersHandler(tornado.web.RequestHandler):
    def get(self):
        """List available exporters"""

        exporters = {}
        for ep in entry_points().select(group="mfr.exporters"):
            exporters.update({ep.name: ep.load().__name__})

        self.write(
            {
                "exporters": exporters,
            }
        )
