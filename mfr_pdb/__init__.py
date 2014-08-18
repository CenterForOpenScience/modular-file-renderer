from mfr.core import FileHandler, get_file_extension
from mfr_pdb.render import render_html

EXTENSIONS = [
    '.pdb',
]


class Handler(FileHandler):
    """The pdb file handler"""

    renderers = {
        'html': render_html
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
