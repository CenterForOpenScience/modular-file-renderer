import os

from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.utils import munge_url_for_localdev, escape_url_for_template


class VideoRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        download_url = munge_url_for_localdev(self.metadata.download_url)
        safe_url = escape_url_for_template(download_url.geturl())
        return self.TEMPLATE.render(url=safe_url)

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
