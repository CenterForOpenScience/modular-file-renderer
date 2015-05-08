# -*- coding: utf-8 -*-

from mfr.core_methods import FileHandler, get_file_extension
from .render import DocxProvider

try:  # requires pydocx
    from .render import render_docx
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
