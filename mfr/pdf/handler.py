# -*- coding: utf-8 -*-

import os
from mako.lookup import TemplateLookup

from mfr.core import FileHandler, get_file_extension
from mfr.pdf.render import render_html

from mfr.pdf.export import PdfExporter

EXTENSIONS = [
    '.pdf'
]

template_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'templates'
    )
)

class PdfFileHandler(FileHandler):

    # TODO: WWSD
    TEMPLATE_LOOKUP = TemplateLookup(directories=[template_path])


    # Renderers and exporters can be callables
    renderers = {
        # like functions
        'html': render_html,
    }

    exporters = {
        # Or instance methods
        'docx': PdfExporter().export_docx,
        'text': PdfExporter().export_txt,
        # ...
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
