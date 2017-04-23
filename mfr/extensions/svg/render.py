"""SVG Image renderer module."""
import os

from mako.lookup import TemplateLookup

from mfr.core import extension


class SvgRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):

        with open(self.file_path, 'r') as fp:
            svg = fp.read()

        return self.TEMPLATE.render(base=self.assets_url, svg=svg)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return False
