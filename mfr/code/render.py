"""code renderer module."""

import pygments
import pygments.lexers
import pygments.formatters

def render_html(fp, *args, **kwargs):
    formatter = pygments.formatters.HtmlFormatter()
    content = fp.read()
    lexer = pygments.lexers.guess_lexer_for_filename(
        fp.name, content)
    highlight = pygments.highlight(content, lexer, formatter)
    # TODO(sloria): Use static path from config
    link = 'href="static/code/css/style.css" />'#.format(self.STATIC_PATH)
    return '<link rel="stylesheet"' + link + '\n' + highlight
