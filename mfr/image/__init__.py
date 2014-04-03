# -*- coding: utf-8 -*-

from mfr.core import FileHandler
from mfr.image.render import render_img_tag

from mfr.image.export import ImageExporter


class ImageFileHandler(FileHandler):

    renderers = {
        'html': render_img_tag,
    }

    exporters = {
        'png': ImageExporter().export_png,
        'jpg': ImageExporter().export_jpg,
        # ...
    }
