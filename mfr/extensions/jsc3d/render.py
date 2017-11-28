"""3D renderer module """
# Uses jsc3d: https://github.com/humu2009/jsc3d/tree/master/jsc3d
import os

import furl
from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.jsc3d import settings
from mfr.extensions.utils import munge_url_for_localdev


class JSC3DRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    @munge_url_for_localdev
    def render(self):
        self.metrics.add('needs_export', False)
        if self.metadata.ext in settings.EXPORT_EXCLUSIONS:
            return self.TEMPLATE.render(
                base=self.assets_url,
                url=self.download_url.geturl(),
                ext=self.metadata.ext.lower(),
            )

        exported_url = furl.furl(self.export_url)
        exported_url.args['format'] = settings.EXPORT_TYPE
        self.metrics.add('needs_export', True)
        return self.TEMPLATE.render(
            base=self.assets_url,
            url=exported_url.url,
            ext=settings.EXPORT_TYPE,
        )

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
