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
        if self.metadata.ext in settings.EXPORT_EXCLUSIONS:
            return self.TEMPLATE.render(base=self.assets_url, url=self.url)

        exported_url = furl.furl(self.export_url)
        if settings.EXPORT_MAXIMUM_SIZE and settings.EXPORT_TYPE:
            exported_url.args['format'] = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        elif settings.EXPORT_TYPE:
            exported_url.args['format'] = settings.EXPORT_TYPE
        else:
            return self.TEMPLATE.render(base=self.assets_url, url=self.url)

        return self.TEMPLATE.render(base=self.assets_url, url=exported_url.url)

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
