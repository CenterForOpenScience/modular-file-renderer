"""GEO renderer module."""
from mfr.core import RenderResult

with open('mfr_geo/templates/geo_template.html') as fid:
    template = fid.read()

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

    content = template.format(geo_json = fp.read(), geo_filename = fp.name)
    return RenderResult(content, assets=get_assets()) 
