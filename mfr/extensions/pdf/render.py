import logging
import os

import furl
from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.pdf import settings
from mfr.extensions.utils import munge_url_for_localdev, escape_url_for_template
from mfr.settings import GOOGLE_ANALYTICS_TRACKING_ID

logger = logging.getLogger(__name__)


class PdfRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):

        download_url = munge_url_for_localdev(self.metadata.download_url)
        escaped_name = escape_url_for_template(
            '{}{}'.format(self.metadata.name, self.metadata.ext)
        )
        logger.debug('extension::{}  supported-list::{}'.format(self.metadata.ext,
                                                                settings.EXPORT_SUPPORTED))
        if self.metadata.ext.lower() not in settings.EXPORT_SUPPORTED:
            logger.debug('Extension not found in supported list!')
            return self.TEMPLATE.render(
                ga_tracking_id=GOOGLE_ANALYTICS_TRACKING_ID,
                base=self.assets_url,
                url=escape_url_for_template(download_url.geturl()),
                stable_id=self.metadata.stable_id,
                file_name=escaped_name,
                enable_hypothesis=settings.ENABLE_HYPOTHESIS,
            )

        logger.debug('Extension found in supported list!')
        exported_url = furl.furl(self.export_url)
        if settings.EXPORT_MAXIMUM_SIZE:
            exported_url.args['format'] = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE,
                                                         settings.EXPORT_TYPE)
        else:
            exported_url.args['format'] = settings.EXPORT_TYPE

        self.metrics.add('needs_export', True)
        return self.TEMPLATE.render(
            ga_tracking_id=GOOGLE_ANALYTICS_TRACKING_ID,
            base=self.assets_url,
            url=escape_url_for_template(exported_url.url),
            stable_id=self.metadata.stable_id,
            file_name=escaped_name,
            enable_hypothesis=settings.ENABLE_HYPOTHESIS,
        )

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
