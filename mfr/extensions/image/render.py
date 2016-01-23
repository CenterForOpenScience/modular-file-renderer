import os

import furl

from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.image import settings


class ImageRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        exported_url = furl.furl(self.export_url)
        exported_url.args['format'] = '{}.{}'.format(settings.MAXIMUM_SIZE, settings.TYPE)
        return self.TEMPLATE.render(base=self.assets_url, url=exported_url.url)

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
