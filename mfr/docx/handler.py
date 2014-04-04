# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension
from mfr.docx.render import render_html

from mfr.docx.export import DocxExporter

EXTENSIONS = [
    '.docx',
    # TODO: finish this list
]


class DocxFileHandler(FileHandler):
    # Renderers and exporters can be callables
    renderers = {
        # like functions
        'html': render_html,
    }

    exporters = {
        # Or instance methods
        'pdf': DocxExporter().export_pdf,
        'txt': DocxExporter().export_txt,
        # ...
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS