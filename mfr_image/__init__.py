# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_image.render import render_img_tag

EXTENSIONS = [
    '.jpeg',
    '.jpg',
    '.png',
    '.bmp',
    '.gif',
]


class Handler(FileHandler):
    """The image file handler."""
    name = "Image"
    renderers = {
        'html': render_img_tag,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
