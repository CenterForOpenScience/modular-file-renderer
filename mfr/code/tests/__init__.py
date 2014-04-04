
from mfr import core
from mfr.code.render import render_html


class codeHandler(core.FileHandler):

    renderer = {'html': render_code_tag}
