# -*- coding: utf-8 -*-
from mfr.core import FileHandler, get_file_extension
from mfr_movie.render import render_movie_tag

EXTENSIONS = [
    '.mp4',
    '.avi',
    '.ogv',
    '.wmv',
    '.webm',
]


class Handler(FileHandler):
    """The movie file handler."""

    renderers = {
        'html': render_movie_tag,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
