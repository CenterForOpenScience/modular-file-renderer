# -*- coding: utf-8 -*-
"""Docx renderer module."""
import sys

from mfr.core import extension

if not sys.version_info >= (3, 0):
    from pydocx.parsers import Docx2Html

    # Workaround to remove default stylesheet and inlined styles
    # see: https://github.com/CenterForOpenScience/pydocx/issues/102
    class MFRDocx2Html(Docx2Html):
        def style(self):
            return ''

        def indent(self, text, *args, **kwargs):
            return text

    def render_docx(fp, *args, **kwargs):
        """Generate an html representation of the docx file using PyDocx

        :param fp: File pointer
        :return: RenderResult object containing the content html
        """
        content = MFRDocx2Html(fp).parsed

class DocxRenderer(extension.BaseRenderer):

    def render(self):
        pass
