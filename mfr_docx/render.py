"""Docx renderer module."""

import pydocx
from mfr import RenderResult

def render_docx(fp, *args, **kwargs):
    return RenderResult(pydocx.Docx2Html(fp).parsed)
