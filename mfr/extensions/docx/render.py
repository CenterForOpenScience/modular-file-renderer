# -*- coding: utf-8 -*-
"""Docx renderer module."""
from mfr.core import extension
from mfr.extensions.docx.convert import render_docx

class DocxRenderer(extension.BaseRenderer):

    def render(self):
        with open(self.file_path, 'r') as fp:
            return render_docx(fp)

    @property
    def requires_file(self):
        return True
