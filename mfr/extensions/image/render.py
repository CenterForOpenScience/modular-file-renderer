"""Image renderer module."""
from mfr.core import extension


class ImageRenderer(extension.BaseRenderer):

    def render(self):
        return '<img src="{src}" />'.format(src=self.url)

    @property
    def requires_file(self):
        return False
