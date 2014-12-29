# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_image.render import render_img_tag

try:  # Exporter requires PIL
    from mfr_image.export import ImageExporter
    exporter = ImageExporter()
    exporters = {
        'png': exporter.export_png,
        'jpeg': exporter.export_jpeg,
        'gif': exporter.export_gif,
        'tif': exporter.export_tif,
    }
except ImportError:
    exporters = {}

EXTENSIONS = [
    '.jpeg',
    '.jpg',
    '.png',
    '.bmp',
    '.gif',
    '.tif',
]


class Handler(FileHandler):
    """FileHandler for image files."""
    renderers = {
        'html': render_img_tag,
    }
    exporters = exporters

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
