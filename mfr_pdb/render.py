from mfr.core import RenderResult
from mako.lookup import TemplateLookup

template = TemplateLookup(
    directories=['mfr_pdb/templates']
).get_template('pdb.mako')


def render_html(fp, **kwargs):
    print kwargs
    content = template.render(pdb_file=fp.read())
    return RenderResult(content)
