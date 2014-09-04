import os
import mfr
from mfr.core import RenderResult, get_assets_from_list

# assets must be loaded in this order
JS_ASSETS = [
    "jquery-1.7.min.js",
    "Three49custom.js",
    "GLmol.js",
]

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'templates', 'pdb.html')


def render_html(fp, **kwargs):

    with open(TEMPLATE) as template:
        content = template.read().format(pdb_file=fp.read())

    assets_uri_base = '{0}/mfr_pdb'.format(mfr.config['STATIC_URL'])

    assets = {
        'js': get_assets_from_list(assets_uri_base, 'js', JS_ASSETS)
    }

    return RenderResult(content, assets)
