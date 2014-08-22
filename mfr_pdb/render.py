import mfr
from mfr.core import RenderResult
from mako.lookup import TemplateLookup

template = TemplateLookup(
    directories=['mfr_pdb/templates']
).get_template('pdb.mako')


def render_html(fp, **kwargs):
    content = template.render(pdb_file=fp.read())

    assets_uri_base = '{0}/mfr_pdb'.format(mfr.config['STATIC_URL'])
    # assets must be loaded in this order
    js_assets = [
        "jquery-1.7.min.js",
        "Three49custom.js",
        "GLmol.js",
    ]

    assets = {
        'js': ['{0}/{1}/{2}'.format(assets_uri_base, 'js', filepath)
               for filepath in js_assets]
    }

    return RenderResult(content, assets)
