from .. import FileRenderer
import os
import pygments
import pygments.lexers
import pygments.formatters
from flask import render_template, request
import json
from flask import jsonify

formatter = pygments.formatters.HtmlFormatter()

class CodeRenderer(FileRenderer):

    def detect(self, fp):
        fname = fp.name
        code_exts_dict = eval(open(os.getcwd() + "/renderer/code/highlightable.txt").read())
        code_exts = list(code_exts_dict.keys())
        for ext in code_exts:
            if fname.endswith(ext):


                #########
                ########
                #todo this is breaking because it wants to read csv files, wtf? turn it back to true
                return True
                #########
                ########
        return False

    def render(self, fp, path):
        content = fp.read()
        highlight = pygments.highlight(
            content,
            pygments.lexers.guess_lexer_for_filename(fp.name, content),
            formatter
        )
        return '<br></br><link rel="stylesheet" href="/static/code/css/style.css" />' + '\n' + highlight

    def edit(self, fp, path):
        fname = fp.name
        code_exts_dict = eval(open(os.getcwd() + "/renderer/code/highlightable.txt").read())
        code_exts = list(code_exts_dict.keys())
        #todo this does not always get the right extension...
        for ext in code_exts:
            if fname.endswith(ext):
                code_ext = ext
        return render_template("code.html", syntax = code_exts_dict[code_ext], editor_content = fp.read())

    def save(self, fp, path):
        filename = str(os.path.split(fp.name)[1])
        file = open("examples/{}".format(filename),'w')
        file.write(str(request.json))
        file.close()
        return ""

    def export_edit(self,fp):
        return fp.read(), 'edit'