from .. import FileRenderer
from flask import render_template
import os
class PdbRenderer(FileRenderer):

    def _detect(self, file_pointer):
        _, ext = os.path.splitext(file_pointer.name)
        return ext.lower() == ".pdb"

    def _render(self, file_pointer, **kwargs):
        return self._render_mako(
            "pdb.mako",
            pdb_file=file_pointer.read(),
        )