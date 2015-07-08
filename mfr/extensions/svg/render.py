"""SVG Image renderer module."""
from mako.lookup import TemplateLookup

from mfr.core import extension, TEMPLATE_BASE

class SvgRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            TEMPLATE_BASE
        ]).get_template('svg_viewer.mako')

    def render(self):
        return self.TEMPLATE.render(base=self.assets_url, url=self.url, md5 = self.extra.get('md5'))

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
