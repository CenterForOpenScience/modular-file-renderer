from .. import FileRenderer
import os
from flask import redirect, request
from docx2html import convert

class DocxRenderer(FileRenderer):

    def detect(self, fp):
        fname = fp.name
        for ext in ['docx']:
            if fname.endswith(ext):
                return True
        return False

    def render(self, fp, path):
        html = convert( os.getcwd() + '/' + fp.name )
        return '<br></br><pre>{}</pre>'.format(html)

    def edit(self, fp, path):
        fname = fp.name
        html_from_file = open(os.getcwd() + "/renderer/docx/text.html").read()
        html = convert( os.getcwd() + '/' + fp.name )
        html_with_data = html_from_file % html
        return html_with_data

    # actually exports html
    def export_text(self, fp):
        html = convert( os.getcwd() + '/' + fp.name )
        return html, '.txt'

    def export_edit(self,fp):
        return fp.read(), 'edit'

    # this will not write docx!
    def save(self, fp, path):
        filename = str(os.path.split(fp.name)[1])
        file = open("examples/{}".format(filename),'w')
        file.write(str(request.json))
        file.close()
        return ""
