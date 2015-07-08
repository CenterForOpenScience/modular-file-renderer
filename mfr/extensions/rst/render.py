import os

from mako.lookup import TemplateLookup
from docutils.core import publish_parts

from mfr.core import extension


class RstRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        with open(self.file_path, 'r') as fp:
            body = publish_parts(fp.read(), writer_name='html')['html_body']
            return self.TEMPLATE.render(base=self.assets_url, body=body, md5 = self.extra.get('md5'))

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
