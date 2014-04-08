# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension
from mfr.image.render import render_img_tag
try:  # Exporter requires PIL
    from mfr.image.export import ImageExporter
    exporters = {
        'png': ImageExporter().export_png,
        'jpg': ImageExporter().export_jpg,
        'gif': ImageExporter().export_gif,
        'tif': ImageExporter().export_tif,
    }
except ImportError:
    exporters = {}

EXTENSIONS = [
    '.jpeg',
    '.jpg',
    '.png',
    '.bmp',
    '.gif',
    #todo (ajs) figure out why tiffs never work...
]


class ImageFileHandler(FileHandler):
    # Renderers and exporters are callables
    renderers = {
        'html': render_img_tag,
    }

    exporters = exporters

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
