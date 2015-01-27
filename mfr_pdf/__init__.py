# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_pdf.render import render_pdf


EXTENSIONS = ['.pdf']


class Handler(FileHandler):

    renderers = {
        'html': render_pdf,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
