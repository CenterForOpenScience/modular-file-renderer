"""PDF renderer module."""
from mfr.core import RenderResult
import PyPDF2
import urllib
import mfr


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
    url_encoded_src = urllib.quote_plus(src)

    assets_uri_base = '{0}/pdf'.format(mfr.config['ASSETS_URL'])

    if is_valid(fp):
        content = (
            '<iframe src="{base}/web/viewer.html?file={src}" width="100%" height="600px"></iframe>'
        ).format(src=url_encoded_src, base=assets_uri_base)
        return RenderResult(content)
    else:
        return RenderResult("This is not a valid pdf file")


