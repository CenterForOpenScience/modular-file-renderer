# -*- coding: utf-8 -*-

"""Docx renderer module."""
import sys

if not sys.version_info >= (3, 0):
    from pydocx.parsers import Docx2Html
    from mfr import RenderResult

    class MFRDocx2HtmlParser(Docx2Html):
        def head(self):
            return ''

        def footer(self):
            return ''

    def render_docx(fp, *args, **kwargs):
        """Generate an html representation of the docx file using PyDocx

        :param fp: File pointer
        :return: RenderResult object containing the content html
        """
        content = MFRDocx2HtmlParser(fp).parsed
        return RenderResult(content=content)
