"""Docx renderer module."""
from mfr import RenderResult
import pydocx


def render_docx(fp, *args, **kwargs):
    return RenderResult(pydocx.Docx2Html(fp).parsed)
