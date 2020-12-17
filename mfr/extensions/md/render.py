import os

from mako.lookup import TemplateLookup

from mfr.core.extension import BaseRenderer


class MdRenderer(BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self):
        """Render a markdown file to html."""
        return self.TEMPLATE.render(base=self.assets_url, url=self.metadata.download_url)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
