# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
try:
    from .render import render_html
except ImportError:
    render_html = None

EXTENSIONS = [
    '.md',
    '.markdown',
]


class Handler(FileHandler):
    """FileHandler for Markdown files"""
    renderers = {
        'html': render_html,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS