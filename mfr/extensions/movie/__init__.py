# -*- coding: utf-8 -*-
from mfr.core_methods import FileHandler, get_file_extension
from .render import render_movie_tag

EXTENSIONS = [
    '.mp4',
    #'.avi',
    '.ogv',
    #'.wmv',
    '.webm',
]


class Handler(FileHandler):
    """FileHandler for video files."""

    renderers = {
        'html': render_movie_tag,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
