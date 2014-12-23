# -*- coding: utf-8 -*-
"""Image exporter module."""
import tempfile
from PIL import Image


class ImageExporter(object):

    def export_png(self, fp):
        temp = tempfile.NamedTemporaryFile(suffix='.png')
        im = Image.open(fp)
        im.save(temp, format='png')
        temp.seek(0)
        return temp

    def export_jpeg(self, fp):
        temp = tempfile.NamedTemporaryFile(suffix='.jpeg')
        im = Image.open(fp)
        im.save(temp, format='jpeg')
        temp.seek(0)
        return temp

    def export_gif(self, fp):
        temp = tempfile.NamedTemporaryFile(suffix='.gif')
        im = Image.open(fp)
        im.save(temp, format='gif')
        temp.seek(0)
        return temp

    def export_tif(self, fp):
        temp = tempfile.NamedTemporaryFile(suffix='.tif')
        im = Image.open(fp)
        im.save(temp, format='tiff')
        temp.seek(0)
        return temp
