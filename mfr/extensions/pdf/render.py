import os

from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.utils import munge_url_for_localdev


class PdfRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        download_url = munge_url_for_localdev(self.metadata.download_url)
        return self.TEMPLATE.render(base=self.assets_url, url=download_url.geturl())

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
