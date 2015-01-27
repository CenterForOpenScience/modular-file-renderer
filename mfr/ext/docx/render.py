# -*- coding: utf-8 -*-

"""Docx renderer module."""
import sys

if not sys.version_info >= (3, 0):
    from pydocx.parsers import Docx2Html
    from mfr import RenderResult

    def render_docx(fp, *args, **kwargs):
        """Generate an html representation of the docx file using PyDocx

        :param fp: File pointer
        :return: RenderResult object containing the content html
        """
        content = Docx2Html(fp).parsed_without_head
        return RenderResult(content=content.encode('ascii', 'ignore'), assets={})
