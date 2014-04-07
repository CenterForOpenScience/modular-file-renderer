# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension
from mfr.ipynb.render import render_html
try:  # Exporter requires PIL
    from mfr.Ipynb.export import IpynbExporter
    exporters = {
        'python': IpynbExporter().export_python,
    }
except ImportError:
    exporters = {}

EXTENSIONS = [
    '.ipynb'
]

class IpynbFileHandler(FileHandler):
    # Renderers and exporters are callables
    renderers = {
        'html': render_html,
    }

    exporters = exporters

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
