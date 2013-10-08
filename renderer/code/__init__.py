from .. import FileRenderer

import pygments
import pygments.lexers
import pygments.formatters

formatter = pygments.formatters.HtmlFormatter()
style = '<style>\n{}\n</style>'.format(formatter.get_style_defs('.highlight'))

class CodeRenderer(FileRenderer):

    def detect(self, fp):
        fname = fp.name
        for ext in ['py', 'rb']:
            if fname.endswith(ext):
                return True
        return False

    def render(self, fp, path):
        content = fp.read()
        highlight = pygments.highlight(
            content,
            pygments.lexers.guess_lexer_for_filename(fp.name, content),
            formatter
        )
        return style + '\n' + highlight
