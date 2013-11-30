from .. import FileRenderer
import os
from flask import redirect, request
class TextRenderer(FileRenderer):

    def detect(self, fp):
        fname = fp.name
        for ext in ['narg']:
            if fname.endswith(ext):
                return True
        return False

    def render(self, fp, path):
        fname = fp.name
        return '<br></br><pre>{}</pre>'.format(fp.read())

    def edit(self, fp, path):
        fname = fp.name
        html_from_file = open(os.getcwd() + "/renderer/text/text.html").read()
        html_with_data = html_from_file % str(fp.read())
        return html_with_data

    def export_text(self, fp):
        return fp.read(), '.txt'

    def export_blah(self, fp):
        return fp.read(), '.bla'

    def export_edit(self,fp):
        return fp.read(), 'edit'

    def save(self, fp, path):
        filename = str(os.path.split(fp.name)[1])
        file = open("examples/{}".format(filename),'w')
        file.write(str(request.json))
        file.close()
        return ""