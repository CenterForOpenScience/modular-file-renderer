# -*- coding: utf-8 -*-

from mfr.core import FileHandler
from mfr.image.render import render_img_tag

from mfr.image.export import ImageExporter


class ImageFileHandler(FileHandler):
    # Renderers and exporters can be callables
    renderers = {
        # like functions
        'html': render_img_tag,
    }

    exporters = {
        # Or instance methods
        'png': ImageExporter().export_png,
        'jpg': ImageExporter().export_jpg,
        # ...
    }
