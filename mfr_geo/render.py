"""GEO renderer module."""
from mfr.core import RenderResult
from jinja2 import Template

with open('mfr_geo/templates/geo_base_template.html') as fid:
    template = Template(fid.read())

def get_assets():
    """Creates a dictionary of js and css assets"""

    static_dir = "/static/mfr/mfr_pdf"

    assets = {}
    assets['js']  = [static_dir + '/js/mapbox.js']
    assets['css'] = [static_dir + '/css/mapbox.css']

    return assets

def render_geo(fp, src=None):
    """A simple geographic (geo) file renderer.

    :param str:
    """

    content = template.render(geo_json = fp.read(), geo_filename = fp.name)
    return RenderResult(content, assets=get_assets()) 
