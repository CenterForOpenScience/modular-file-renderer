# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_geo.render import render_geo

EXTENSIONS = ['.geojson']

#TODO: add support for ESRI shapefile (shp), well known text (wkt), etc...

class Handler(FileHandler):
    """The geo file handler."""

    renderers = {
        'html': render_geo,
    }

    exporters = {}

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
