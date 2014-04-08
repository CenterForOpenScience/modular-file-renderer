# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension
try:
    from mfr.rst.render import render_rst
    renderers = {
        'html': render_rst
    }
except ImportError:
    renderers = {}

EXTENSIONS = [
    '.rst',
]


class RstFileHandler(FileHandler):
    # Renderers and exporters can be callables
    renderers = renderers

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
