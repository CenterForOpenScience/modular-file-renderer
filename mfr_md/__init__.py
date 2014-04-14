# -*- coding: utf-8 -*-
"""Markdown support for mfr."""

from mfr.core import FileHandler, get_file_extension
from mfr_md.render import render_html

class Handler(FileHandler):
    renderers = {
        'html': render_html,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in ['.markdown', '.md', ]
