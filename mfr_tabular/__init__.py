# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_tabular.render import render_html

EXTENSIONS = [
    '.csv',
    '.tsv',
    '.xls',
]


class Handler(FileHandler):
    renderers = {
        'html':  render_html
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
