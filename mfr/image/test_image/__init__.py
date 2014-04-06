
from mfr import core
from mfr.image.render import render_img_tag


class ImageHandler(core.FileHandler):

    renderer = {'html': render_img_tag}
