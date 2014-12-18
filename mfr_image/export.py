# -*- coding: utf-8 -*-
"""Image exporter module."""
import tempfile
from PIL import Image


class ImageExporter(object):

    def export_png(self, fp):
        temp = tempfile.NamedTemporaryFile()
        im = Image.open(fp)
        im.save(temp, format='png')
        temp.seek(0)
        return temp

    def export_jpg(self, fp):
        temp = tempfile.NamedTemporaryFile()
        im = Image.open(fp)
        im.save(temp, format='jpg')
        temp.seek(0)
        return temp

    def export_gif(self, fp):
        temp = tempfile.NamedTemporaryFile()
        im = Image.open(fp)
        im.save(temp, format='gif')
        temp.seek(0)
        return temp

    def export_tif(self, fp):
        temp = tempfile.NamedTemporaryFile()
        im = Image.open(fp)
        im.save(temp, format='tiff')
        temp.seek(0)
        return temp
