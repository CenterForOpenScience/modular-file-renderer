"""Molecule renderer module """
#Uses PV: https://github.com/biasmv/pv
import os
import mfr

from mako.lookup import TemplateLookup
from mfr.core import extension


TEMPLATE = TemplateLookup(
    directories=[os.path.join(os.path.dirname(__file__),
        'templates')]).get_template('viewer.mako')

# assets must be loaded in this order
#JS_ASSETS = [
    #The OSF has jquery on each page
    #'jquery-1.7.min.js',
#]

def get_assets():
    assets_uri_base = '{0}/pdb'.format(mfr.config['ASSETS_URL'])

    assets = {
  #      'js': get_assets_from_list(assets_uri_base, 'js', JS_ASSETS)
    }

    return assets

class PdbRenderer(extension.BaseRenderer):

    def render(self):
        return TEMPLATE.render(url=self.url, base=self.assets_url)
        #TEMPLATE.render(url=self.file_path)

    @property
    def requires_file(self):
        return True
