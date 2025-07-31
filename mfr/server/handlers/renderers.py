from importlib.metadata import entry_points

import tornado.web


class RenderersHandler(tornado.web.RequestHandler):
    def get(self):
        """List available renderers"""

        renderers = {}
        for ep in entry_points().select(group="mfr.renderers"):
            renderers.update({ep.name: ep.load().__name__})

        self.write(
            {
                "renderers": renderers,
            }
        )
