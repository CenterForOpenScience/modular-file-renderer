from mfr.core import RenderResult
from mako.lookup import TemplateLookup

template = TemplateLookup(
    directories=['mfr_pdb/templates']
).get_template('pdb.mako')


def render_html(fp, **kwargs):
    content = template.render(pdb_file=fp.read())

    # assets must be loaded in this order
    assets = {
        'js': [
            "/static/mfr/mfr_pdb/js/jquery-1.7.min.js",
            "/static/mfr/mfr_pdb/js/Three49custom.js",
            "/static/mfr/mfr_pdb/js/GLmol.js",
        ]
    }

    return RenderResult(content, assets)
