"""PDF renderer module."""
from mfr.core import RenderResult
from mako.lookup import TemplateLookup
from mfr import config as core_config
import os
import PyPDF2


template = TemplateLookup(
    directories=[os.path.join(os.path.dirname(__file__),
        'templates')]).get_template("pdfpage.mako")

JS_ASSETS = [
    "pdf.js",
    "compatibility.js",
    #"jquery.min.js",
]


def get_assets():
    """Creates a dictionary of js and css assets"""
    assets_uri_base = '{0}/pdf'.format(mfr.config['ASSETS_URL'])
    assets = {}
    jspath = '{base}/js/{fname}')
    assets['js'] = [jspath.format(base=assets_uri_base, fname=fname)
                    for fname in JS_ASSETS]
    return assets


def is_valid(fp):
    """Tests file pointer for validity

    :return: True if fp is a valid pdf, False if not
    """
    try:
        PyPDF2.PdfFileReader(fp)
        return True
    except PyPDF2.utils.PdfReadError:
        return False

def render_pdf(fp, src=None):
    """A simple pdf renderer.

    :param fp: File pointer
    :param src: Path to file
    :return: A RenderResult object containing html content and js assets for pdf rendering
    """
    src = src or fp.name

    if is_valid(fp):
        content = template.render(url=src, STATIC_PATH=core_config['ASSETS_URL'])
        return RenderResult(content, assets=get_assets())
    else:
        return RenderResult("This is not a valid pdf file")
