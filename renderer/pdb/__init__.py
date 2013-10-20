from .. import FileRenderer
from flask import render_template

class PdbRenderer(FileRenderer):

    def detect(self, fp):
        fname = fp.name
        for ext in ['pdb']:
            if fname.endswith(ext):
                return True
        return False

    def render(self, fp, path):
        fname = fp.name
        pdb_id = fname.split('.')[0]
        return render_template('pdb/pdbviewer.html', pdb_file=fp.read())

    def export_pdb(self, fp):
        return fp.read(), '.pdb'