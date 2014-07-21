"""Docx renderer module."""

import pydocx
from mfr import RenderResult


def render_docx(fp, *args, **kwargs):
    return RenderResult(content=pydocx.Docx2Html(fp.name).parsed, assets={})
