"""Molecule renderer module """
import os
import json

from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.pdb import settings
from mfr.extensions.utils import munge_url_for_localdev


class PdbRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    @munge_url_for_localdev
    def render(self):
        return self.TEMPLATE.render(
            base=self.assets_url,
            url=self.download_url.geturl(),
            options=json.dumps(settings.OPTIONS),
        )

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
