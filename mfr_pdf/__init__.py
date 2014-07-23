# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_pdf.render import render_pdf_mako

class Handler(FileHandler):
    """The image file handler."""
    renderers = {
        'html': render_img_tag,
    }
    exporters = exporters

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS

