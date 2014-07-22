"""Docx renderer module."""

import pydocx
from mfr import RenderResult


def render_docx(fp, *args, **kwargs):
    content = pydocx.Docx2Html(fp).parsed
    return RenderResult(content=content, assets={})
