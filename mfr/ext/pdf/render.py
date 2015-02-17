"""PDF renderer module."""
from mfr.core import RenderResult
import PyPDF2


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
        print str(fp)
        content = '<iframe src="/static/mfr/pdf/web/viewer.html?file=%2Fstatic%2Fmfr%2Fpdf%2Ftest%2FLecture.pdf" width="100%" height="600px"/>'
        return RenderResult(content)
    else:
        return RenderResult("This is not a valid pdf file")
