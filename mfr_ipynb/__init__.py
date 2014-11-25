# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
try:
    from mfr_ipynb.render import render_html
except ImportError:
    render_html = None

EXTENSIONS = [
    '.ipynb'
]


class Handler(FileHandler):
    renderers = {
        'html': render_html,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
