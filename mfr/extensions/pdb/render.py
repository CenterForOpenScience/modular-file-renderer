"""Molecule renderer module """
import os

from mako.lookup import TemplateLookup
from mfr.core import extension


TEMPLATE = TemplateLookup(
    directories=[os.path.join(os.path.dirname(__file__),
        'templates')]).get_template('viewer.mako')


class PdbRenderer(extension.BaseRenderer):

    def render(self):
        return TEMPLATE.render(url=self.url, base=self.assets_url)

    @property
    def requires_file(self):
        return True
