# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_image.render import render_img_tag

try:  # Exporter requires PIL
    from mfr_image.export import ImageExporter
    exporter = ImageExporter()
    exporters = {
        # 'png': exporter.export_png,
        'jpg': exporter.export_jpg,
        'gif': exporter.export_gif,
        # 'tif': exporter.export_tif,
    }
except ImportError:
    exporters = {}

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

    exporters = exporters

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
