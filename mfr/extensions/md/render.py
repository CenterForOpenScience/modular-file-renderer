import os

import bleach
from mako.lookup import TemplateLookup

from mfr.core import extension


class MdRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self):
        """Render a markdown file to html."""
        with open(self.file_path, 'r') as fp:
            body = fp.read()
            return self.TEMPLATE.render(base=self.assets_url, body=body)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
