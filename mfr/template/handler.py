# -*- coding: utf-8 -*-

from mfr.template.render import render_html
from mfr.core import FileHandler, get_file_extension

try:
    from mfr.template.export import TEMPLATEExporter
    exporters = {
        'sample': TEMPLATEExporter().export_SAMPLE,
    }
except ImportError:
    exporters = {}

""" Defines extensions this module should detect """
EXTENSIONS = [
    '.SAMPLE',
    '.TEST',
]


class TEMPLATEFileHandler(FileHandler):
    # Renderers and exporters are callables
    renderers = {
        'html': render_html,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
