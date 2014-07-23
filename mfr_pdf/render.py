"""PDF renderer module."""
from mfr.core import RenderResult
from mako.lookup import TemplateLookup
from mfr import config as core_config
import PyPDF2

template  = TemplateLookup(
            directories=['/templates']
        ).get_template("pdfpage.mako")

def render_pdf_mako(fp, url=None):
    """A simple pdf renderer.

    :param str:
    """
    url = url or fp.name

    content = template.render(url=url,STATIC_PATH=core_config['STATIC_URL'])
    return RenderResult(content)
