"""Docx renderer module."""

import pydocx


def render_docx(fp, *args, **kwargs):
    return pydocx.Docx2Html(fp).parsed
