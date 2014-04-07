
from mfr import core
from mfr.TEMPLATE.render import render_TEMPLATE_tag


class TEMPLATEHandler(core.FileHandler):

    renderer = {'html': render_TEMPLATE_tag}
