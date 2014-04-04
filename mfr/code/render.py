"""code renderer module."""

import pygments
import pygments.lexers
import pygments.formatters

def render_html(fp, src=None, alt=''):
    formatter = pygments.formatters.HtmlFormatter()
    content = fp.read()
    highlight = pygments.highlight(
    content, pygments.lexers.guess_lexer_for_filename(
    fp.name, content), formatter)
    link = 'href="static/code/css/style.css" />'#.format(self.STATIC_PATH)
    return '<link rel="stylesheet"' + link + '\n' + highlight