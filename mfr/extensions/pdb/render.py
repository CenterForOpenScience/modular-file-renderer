"""Molecule renderer module """
import os
import json

from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.pdb import settings


class PdbRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        return self.TEMPLATE.render(
            url=self.url,
            base=self.assets_url,
            min_height=settings.MIN_HEIGHT,
            min_width=settings.MIN_WIDTH,
            options=json.dumps(settings.OPTIONS),
        )

    @property
    def requires_file(self):
        return True
