import os

from mako.lookup import TemplateLookup

from mfr.core import extension


class PdfRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        return self.TEMPLATE.render(base=self.assets_url, url=self.metadata.download_url, md5 = self.extra.get('md5'))

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
