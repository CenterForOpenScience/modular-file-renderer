"""code renderer module."""

import pygments
import pygments.lexers
import pygments.formatters

from mfr import config


def render_html(fp, *args, **kwargs):
    formatter = pygments.formatters.HtmlFormatter()
    content = fp.read()
    lexer = pygments.lexers.guess_lexer_for_filename(
        fp.name, content)
    content = pygments.highlight(content, lexer, formatter)
    if config['INCLUDE_STATIC']:
        link = get_stylesheet()
        return '\n'.join([link, content])
    else:
        return content


def get_stylesheet():
    return '<link rel="stylesheet" href="{0}/mfr_code_pygments/css/style.css" />'\
        .format(config['STATIC_URL'])
