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

    def render(self):
        download_url = munge_url_for_localdev(self.metadata.download_url)
        return self.TEMPLATE.render(
            base=self.assets_url,
            url=download_url.geturl(),
            options=json.dumps(settings.OPTIONS),
        )

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
