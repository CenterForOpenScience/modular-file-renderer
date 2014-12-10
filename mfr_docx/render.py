# -*- coding: utf-8 -*-

"""Docx renderer module."""
import sys

if not sys.version_info >= (3, 0):
    import pydocx
    from mfr import RenderResult

    def render_docx(fp, *args, **kwargs):
        """Generate an html representation of the docx file using PyDocx

        :param fp: File pointer
        :return: RenderResult object containing the content html
        """
        content = pydocx.Docx2Html(fp)._parsed
        return RenderResult(content=content.encode('ascii', 'ignore'), assets={})
