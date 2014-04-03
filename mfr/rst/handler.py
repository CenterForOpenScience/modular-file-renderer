# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension
from mfr.template.render import render_TEMPLATE_tag

from mfr.TEMPLATE.export import TEMPLATEExporter

EXTENSIONS = [
    '.SAMPLE',
    '.TEST',
    # TODO: finish this list
]


class TEMPLATEFileHandler(FileHandler):
    # Renderers and exporters can be callables
    renderers = {
        # like functions
        'html': render_TEMPLATE_tag,
    }

    exporters = {
        # Or instance methods
        'SAMPLE': TEMPLATEExporter().export_SAMPLE,
        'TEST': TEMPLATEExporter().export_TEST,
        # ...
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
