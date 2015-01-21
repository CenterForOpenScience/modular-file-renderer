# -*- coding: utf-8 -*-
"""Image exporter module."""
import tempfile
from PIL import Image


class ImageExporter(object):

    def export_png(self, fp):
        temp = tempfile.NamedTemporaryFile(suffix='.png')
        try:
            im = Image.open(fp)
            im.save(temp, format='png')
            temp.seek(0)
            return temp
        except UnicodeDecodeError as e:
            return "Unable to export: {0}".format(e)

    def export_jpeg(self, fp):
        temp = tempfile.NamedTemporaryFile(suffix='.jpeg')
        try:
            im = Image.open(fp)
            im.save(temp, format='jpeg')
            temp.seek(0)
            return temp
        except UnicodeDecodeError as e:
            return "Unable to export: {0}".format(e)

    def export_gif(self, fp):
        temp = tempfile.NamedTemporaryFile(suffix='.gif')
        try:
            im = Image.open(fp)
            im.save(temp, format='gif')
            temp.seek(0)
            return temp
        except UnicodeDecodeError as e:
            return "Unable to export: {0}".format(e)

    def export_tif(self, fp):
        temp = tempfile.NamedTemporaryFile(suffix='.tif')
        try:
            im = Image.open(fp)
            im.save(temp, format='tiff')
            temp.seek(0)
            return temp
        except UnicodeDecodeError as e:
            return "Unable to export: {0}".format(e)
