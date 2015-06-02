import os

from mako.lookup import TemplateLookup

from mfr.core import extension


class MovieRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        return self.TEMPLATE.render(base=self.assets_url, url=self.url)

    @property
    def requires_file(self):
        return False
