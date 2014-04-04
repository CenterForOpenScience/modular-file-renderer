"""Pdf renderer module."""

import PyPDF2
import os.path

#TODO Fix this because it doesn't actually work :)  The Mako template needs help!!!
temp = PdfFileHandler.TEMPLATE_LOOKUP

def render_template(file_name, **kwargs):
    return temp.get_template(file_name).render(**kwargs)



def render_html(fp, src=None, alt=''):

    if src is None:
        src = fp.name
    return render_template(
        "pdfpage.mako",
        url=src,
        STATIC_PATH='static/'
    )
