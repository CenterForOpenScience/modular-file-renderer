# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_pdf.render import render_pdf


EXTENSIONS = ['.pdf']


class Handler(FileHandler):
    """The pdf file handler."""
    renderers = {
        'html': render_pdf,
    }

    exporters = {}

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
