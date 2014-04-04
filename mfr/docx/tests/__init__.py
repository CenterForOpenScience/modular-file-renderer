
from mfr import core
from mfr.docx.render import render_html


class DocxHandler(core.FileHandler):

    renderer = {'html': render_html}
