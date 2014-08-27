import os
import mfr
from mfr.core import RenderResult
from mako.template import Template


JS_ASSETS = [
    "jquery-1.7.min.js",
    "Three49custom.js",
    "GLmol.js",
]


def render_html(fp, **kwargs):
    HERE = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(HERE, 'templates', 'tabular.mako')
    template = Template(filename=filename)

    content = template.render(pdb_file=fp.read())

    assets_uri_base = '{0}/mfr_pdb'.format(mfr.config['STATIC_URL'])
    # assets must be loaded in this order

    # TODO(asmacdo) replace with mfr.get_assets_from_list
    assets = {
        'js': ['{0}/{1}/{2}'.format(assets_uri_base, 'js', filepath)
               for filepath in JS_ASSETS]
    }

    return RenderResult(content, assets)
