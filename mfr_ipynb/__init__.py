# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension
from mfr_ipynb.render import render_html

EXTENSIONS = [
    '.ipynb'
]


class Handler(FileHandler):

    renderers = {
        'html': render_html,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
