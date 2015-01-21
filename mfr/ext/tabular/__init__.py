# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from .render import render_html

EXTENSIONS = [
    '.csv',
    '.tsv',
    '.xlsx',
    '.xls',
    '.dta',
    '.sav',
    # '.ods',
]


class Handler(FileHandler):
    """FileHandler for tabular data files."""
    renderers = {
        'html': render_html
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
