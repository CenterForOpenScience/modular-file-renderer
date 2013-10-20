from .. import FileRenderer

import pygments
import pygments.lexers
import pygments.formatters

formatter = pygments.formatters.HtmlFormatter()

class CodeRenderer(FileRenderer):

    def detect(self, fp):
        fname = fp.name
        for ext in ['py', 'rb']:
            if fname.endswith(ext):
                return ext
        return ''

    def render(self, fp, path):
        content = fp.read()
        highlight = pygments.highlight(
            content,
            pygments.lexers.guess_lexer_for_filename(fp.name, content),
            formatter
        )
        return '<link rel="stylesheet" href="/static/code/css/style.css" />' + '\n' + highlight
