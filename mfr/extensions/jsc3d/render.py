"""3D renderer module """
# Uses jsc3d: https://code.google.com/p/jsc3d/
import os

from mako.lookup import TemplateLookup
from mfr.core import extension


class StlRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        # import ipdb; ipdb.set_trace()
        return self.TEMPLATE.render(
            base=self.assets_url,
            url=self.metadata.download_url,
            fileExt=self.metadata.ext,
        )

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
