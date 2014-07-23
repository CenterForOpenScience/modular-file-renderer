# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_pdf.render import render_pdf_mako
import PyPDF2

class Handler(FileHandler):
    """The image file handler."""
    renderers = {
        'html': render_img_tag,
    }
    exporters = exporters

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS

class PdfRenderer(FileRenderer):

    # Gets here using the .pdf extension check then attempts to read the file
        # using pydf2, if it can it accepts it as a valid pdf

    def _detect(self, file_pointer):
        _, ext = os.path.splitext(file_pointer.name)
        if ext.lower() == ".pdf":
            try:
                PyPDF2.PdfFileReader(file_pointer)
            except PyPDF2.utils.PdfReadError:
                return False
            return True
        return False

    def _render(self, file_pointer, **kwargs):
        url = kwargs['url']
        return self._render_mako(
            "pdfpage.mako",
            url=url,
            STATIC_PATH=self.STATIC_PATH,
        )
