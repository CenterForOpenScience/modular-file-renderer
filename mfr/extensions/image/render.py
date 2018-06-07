import os

import furl
from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.image import settings
from mfr.extensions.utils import munge_url_for_localdev, escape_url_for_template


class ImageRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        self.metrics.add('needs_export', False)
        if self.metadata.ext in settings.EXPORT_EXCLUSIONS:
            download_url = munge_url_for_localdev(self.url)
            safe_url = escape_url_for_template(download_url.geturl())
            return self.TEMPLATE.render(base=self.assets_url, url=safe_url)

        exported_url = furl.furl(self.export_url)
        if settings.EXPORT_MAXIMUM_SIZE and settings.EXPORT_TYPE:
            exported_url.args['format'] = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        elif settings.EXPORT_TYPE:
            exported_url.args['format'] = settings.EXPORT_TYPE
        else:
            download_url = munge_url_for_localdev(self.url)
            safe_url = escape_url_for_template(download_url.geturl())
            return self.TEMPLATE.render(base=self.assets_url, url=safe_url)

        self.metrics.add('needs_export', True)
        safe_url = escape_url_for_template(exported_url.url)
        return self.TEMPLATE.render(base=self.assets_url, url=safe_url)

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
