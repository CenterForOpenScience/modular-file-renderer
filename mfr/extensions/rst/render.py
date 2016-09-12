import os

import docutils
from docutils.core import publish_parts

from mako.lookup import TemplateLookup

from mfr.core import extension


class RstRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics.add('docutils_version', docutils.__version__)

    def render(self):
        with open(self.file_path, 'r') as fp:
            body = publish_parts(fp.read(), writer_name='html')['html_body']
            return self.TEMPLATE.render(base=self.assets_url, body=body)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
