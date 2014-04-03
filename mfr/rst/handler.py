# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension
from mfr.rst.render import render_html

from mfr.rst.export import RstExporter

EXTENSIONS = [
    '.rst',
]


class RstFileHandler(FileHandler):
    # Renderers and exporters can be callables
    renderers = {
        # like functions
        'html': render_html,
    }

    exporters = {
        # Or instance methods
        'html': RstExporter().export_html,
        'txt': RstExporter().export_txt,
        # ...
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
