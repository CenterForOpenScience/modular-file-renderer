"""GEO renderer module."""
from mfr.core import RenderResult
from jinja2 import Template
import os

with open('mfr_geo/templates/geo_base_template.html') as fid:
    template = Template(fid.read())


def render_geo(fp, src=None):
    """A simple geographic (geo) file renderer.

    :param str:
    """

    content = template.render(geo_json = fp.read(),
                              geo_full_filename = fp.name)
    return RenderResult(content) 
