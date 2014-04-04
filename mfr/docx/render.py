"""TEMPLATE renderer module."""

import pydocx

def render_html(fp, src=None, alt=''):
    return pydocx.Docx2Html(fp).parsed