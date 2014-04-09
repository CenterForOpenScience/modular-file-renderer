# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension

try:  # requires pydocx
    from mfr_docx.render import render_docx
    renderers = {
        'html': render_docx,
    }
except ImportError:
    renderers = {}

EXTENSIONS = [
    '.docx',
]

class Handler(FileHandler):
    """FileHandler for Microsoft Docx files."""
    renderers = renderers

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
