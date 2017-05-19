import os

from mako.lookup import TemplateLookup

from mfr.extensions.utils import download_from_template
from mfr.core import extension


class VideoRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    @download_from_template
    def render(self):
        return self.TEMPLATE.render(url=self.download_url.geturl())

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
