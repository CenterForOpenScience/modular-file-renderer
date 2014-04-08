# -*- coding: utf-8 -*-

from mfr.core import FileHandler, get_file_extension


EXTENSIONS = [
    '.SAMPLE',
    '.TEST',
    # TODO: finish this list
]


class TEMPLATEFileHandler(FileHandler):
    # Renderers and exporters are callables
    renderers = {
        # TODO
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
