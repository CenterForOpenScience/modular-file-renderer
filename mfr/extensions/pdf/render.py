import logging
import os

import furl
from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.pdf import settings
from mfr.extensions.utils import munge_url_for_localdev

logger = logging.getLogger(__name__)


class PdfRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        download_url = munge_url_for_localdev(self.metadata.download_url)
        logger.debug('extension::{}  supported-list::{}'.format(self.metadata.ext, settings.EXPORT_SUPPORTED))
        if self.metadata.ext not in settings.EXPORT_SUPPORTED:
            logger.debug('Extension not found in supported list!')
            return self.TEMPLATE.render(base=self.assets_url, url=download_url.geturl())

        logger.debug('Extension found in supported list!')
        exported_url = furl.furl(self.export_url)
        if settings.EXPORT_TYPE:
            if settings.EXPORT_MAXIMUM_SIZE:
                exported_url.args['format'] = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE,
                                                             settings.EXPORT_TYPE)
            else:
                exported_url.args['format'] = settings.EXPORT_TYPE

            self.metrics.add('needs_export', True)
            return self.TEMPLATE.render(base=self.assets_url, url=exported_url.url)

        return self.TEMPLATE.render(base=self.assets_url, url=download_url.geturl())

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
