"""PDF renderer module."""
from mfr.core import RenderResult
from mako.lookup import TemplateLookup
from mfr import config as core_config
import PyPDF2

template  = TemplateLookup(
    directories=['mfr_pdf/templates']
).get_template("pdfpage.mako")

def render_pdf_mako(fp, src=None):
    """A simple pdf renderer.

    :param str:
    """
    src = src or fp.name

    content = template.render(url=src,STATIC_PATH=core_config['STATIC_URL'])
    return RenderResult(content)
