# -*- coding: utf-8 -*-

"""Docx renderer module."""
import sys

if not sys.version_info >= (3, 0):
    import pydocx
    from mfr import RenderResult

    def render_docx(fp, *args, **kwargs):
        content = pydocx.Docx2Html(fp)._parsed
        return RenderResult(content=content.encode('ascii', 'ignore'), assets={})
