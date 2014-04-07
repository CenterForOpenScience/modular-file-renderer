# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension
from mfr.docx.render import render_html

EXTENSIONS = [
    '.docx',
]


class DocxFileHandler(FileHandler):
    # Renderers and exporters can be callables
    renderers = {
        # like functions
        'html': render_html,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
