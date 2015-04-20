# -*- coding: utf-8 -*-
"""ReStructuredText support for mfr."""

from mfr.core_methods import FileHandler, get_file_extension

try:  # requires docutils
    from .render import render_rst
    renderers = {
        'html': render_rst
    }
except ImportError:
    renderers = {}

EXTENSIONS = [
    '.rst',
]


class Handler(FileHandler):
    """FileHandler for reStructuredText files."""
    # Renderers and exporters can be callables
    renderers = renderers

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
