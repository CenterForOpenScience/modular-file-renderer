# -*- coding: utf-8 -*-
"""Image exporter module."""
from PIL import Image
from cStringIO import StringIO


class ImageExporter(object):

    def export_png(self, fp):
        im = Image.open(fp)
        sio = StringIO()
        im.save(sio, format='png')
        return sio.getvalue()

    def export_jpg(self, fp):
        im = Image.open(fp)
        sio = StringIO()
        im.save(sio, format='jpg')
        return sio.getvalue()

    def export_gif(self, fp):
        im = Image.open(fp)
        sio = StringIO()
        im.save(sio, format='gif')
        return sio.getvalue()

    def export_tif(self, fp):
        im = Image.open(fp)
        sio = StringIO()
        im.save(sio, format='tif')
        return sio.getvalue()