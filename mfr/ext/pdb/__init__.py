from mfr.core import FileHandler, get_file_extension
from .render import render_html

EXTENSIONS = [
    '.pdb',
]


class Handler(FileHandler):
    """FileHandler for Protein Data Bank files."""

    renderers = {
        'html': render_html
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
