# -*- coding: utf-8 -*-
"""Image exporter module."""
from cStringIO import StringIO


class TEMPLATEExporter(object):

    def export_SAMPLE(self, fp):
        """takes a file pointer, converts file to other type and returns a StringIO of the exported file"""
        sio = StringIO()
        return sio.getvalue()

