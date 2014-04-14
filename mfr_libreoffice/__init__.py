# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_libreoffice.render import render

EXTENSIONS = [
    '.doc',
    '.docx',
    '.odt',
    '.ott',
    '.odp',
    '.rtf',
    '.ppt',
    '.pptx',
    '.xls',
    '.xlsx',
    '.csv',
    '.ods',
]


class Handler(FileHandler):
    """The image file handler."""
    renderers = {
        'html': render,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
