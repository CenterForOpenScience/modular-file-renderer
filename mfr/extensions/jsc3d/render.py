"""3D renderer module """
# Uses jsc3d: https://github.com/humu2009/jsc3d/tree/master/jsc3d
import os

from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.utils import munge_url_for_localdev


class JSC3DRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    @munge_url_for_localdev
    def render(self):
        return self.TEMPLATE.render(
            base=self.assets_url,
            url=self.download_url.geturl(),
            ext=self.metadata.ext.lower(),
        )

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
