# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from .render import render_pdf


EXTENSIONS = ['.pdf']


class Handler(FileHandler):
    """FileHandler for Portable Document Format files."""
    renderers = {
        'html': render_pdf,
    }

    exporters = {}

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
