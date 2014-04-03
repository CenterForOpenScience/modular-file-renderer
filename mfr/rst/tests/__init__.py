
from mfr import core
from mfr.rst.render import render_html


class RstHandler(core.FileHandler):

    renderer = {'html': render_html}
