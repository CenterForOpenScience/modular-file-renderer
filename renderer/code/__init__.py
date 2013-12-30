from .. import FileRenderer
import os
import pygments
import pygments.lexers
import pygments.formatters
from flask import render_template, request


class CodeRenderer(FileRenderer):

    def detect(self, file_pointer):
        syntax_by_ext = eval(open(os.getcwd() +
                                  "/renderer/code/syntax.txt").read())
        syntax = list(syntax_by_ext.keys())
        for ext in syntax:
            if file_pointer.name.endswith(ext):
                return True
        return False

    def render(self, file_pointer, file_path):
        formatter = pygments.formatters.HtmlFormatter()
        content = file_pointer.read()
        highlight = pygments.highlight(
            content, pygments.lexers.guess_lexer_for_filename(
                file_pointer.name, content), formatter)

        return '<br></br><link rel="stylesheet" ' \
               'href="/static/code/css/style.css" />' + '\n' + highlight

    def edit(self, file_pointer, file_path):
        syntax_by_ext = eval(open(os.getcwd() +
                                  "/renderer/code/syntax.txt").read())
        syntax = list(syntax_by_ext.keys())
        code_ext = "plaintext"
        for ext in syntax:
            if file_pointer.name.endswith(ext):
                code_ext = ext
                break
        return render_template("code.html", syntax=syntax_by_ext[code_ext],
                               editor_content=file_pointer.read())

    def save(self, file_pointer, file_path):
        _, file_name = os.path.split(file_pointer.name)
        f = open("examples/{}".format(file_name), 'w')
        f.write(str(request.json))
        f.close()
        return ""

    def export_edit(self, file_pointer):
        return file_pointer.read(), 'edit'