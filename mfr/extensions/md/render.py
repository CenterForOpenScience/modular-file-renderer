import os

import bleach
from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.md.settings import BLEACH_WHITELIST

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
            # Bleach will bug out on unclosed tags. OSF wiki does not have this issue.
            # This is due to versioning problems: https://github.com/mozilla/bleach/issues/271
            body = bleach.clean(fp.read(), **BLEACH_WHITELIST)
            return self.TEMPLATE.render(base=self.assets_url, body=body)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
