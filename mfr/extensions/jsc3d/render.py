"""3D renderer module """
# Uses jsc3d: https://github.com/humu2009/jsc3d/tree/master/jsc3d
import os

from mako.lookup import TemplateLookup
from mfr.core import extension


class JSC3DRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        return self.TEMPLATE.render(
            base=self.assets_url,
            url=self.metadata.download_url,
            ext=self.metadata.ext.lower(),
        )

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
