# -*- coding: utf-8 -*-
"""Docx renderer module."""
from mfr.core import extension
from pydocx.export import PyDocXHTMLExporter

class DocxRenderer(extension.BaseRenderer):

    def render(self):
        exporter = PyDocXHTMLExporter(self.file_path)
        html = exporter.parsed
        return html

    @property
    def requires_file(self):
        return False
