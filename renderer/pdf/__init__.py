from .. import FileRenderer
import os


"""
Extract PDF text using PDFMiner. Adapted from
http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from cStringIO import StringIO

def pdf_to_text(fp):
    """Extract text from PDF document.

    :param fp: File pointer containing PDF
    :return: Text in PDF

    """
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text

class PdfRenderer(FileRenderer):

    def detect(self, fp):
        fname = fp.name
        for ext in ['pdf']:
            if fname.endswith(ext):
                return True
        return False

    def render(self, fp, path):
        html_from_file = open(os.getcwd() + "/renderer/pdf/display_pdf.html").read()
        html_with_data = html_from_file % (path)
        return html_with_data

    def export_text(self, fp):
        return pdf_to_text(fp), '.txt'