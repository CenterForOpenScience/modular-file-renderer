"""SVG Image renderer module."""
import os

from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.utils import escape_url_for_template


class SvgRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        safe_url = escape_url_for_template(self.url)
        return self.TEMPLATE.render(base=self.assets_url, url=safe_url)

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
