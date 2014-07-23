# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_pdf.render import render_pdf_mako
import PyPDF2


def is_valid(fp):
    try:
        PyPDF2.PdfFileReader(fp)
        return True
    except PyPDF2.utils.PdfReadError:
        return False


class Handler(FileHandler):
    """The image file handler."""
    renderers = {
        'html': render_pdf_mako,
    }

    exporters = {}

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS and is_valid(fp)
