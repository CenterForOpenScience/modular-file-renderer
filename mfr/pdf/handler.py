# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension
from mfr.pdf.render import render_html

from mfr.pdf.export import PdfExporter

EXTENSIONS = [
    '.SAMPLE',
    '.TEST',
    # TODO: finish this list
]


class PdfFileHandler(FileHandler):
    # Renderers and exporters can be callables
    renderers = {
        # like functions
        'html': render_html,
    }

    exporters = {
        # Or instance methods
        'docx': PdfExporter().export_docx,
        'text': PdfExporter().export_txt(),
        # ...
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
