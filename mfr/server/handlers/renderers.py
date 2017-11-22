import pkg_resources
import tornado.web


class RenderersHandler(tornado.web.RequestHandler):

    def get(self):
        """List available renderers"""

        renderers = {}
        for ep in pkg_resources.iter_entry_points(group='mfr.renderers'):
            renderers.update({ep.name: ep.load().__name__})

        self.write({
            'renderers': renderers,
        })
