"""code renderer module."""

import pygments
import pygments.lexers
import pygments.formatters

from mfr import config as core_config
from mfr import RenderResult

from mfr_code_pygments.configuration import config as module_config


def render_html(fp, *args, **kwargs):
    formatter = pygments.formatters.HtmlFormatter(cssclass=module_config['CSS_CLASS'])
    content = fp.read()
    lexer = pygments.lexers.guess_lexer_for_filename(fp.name, content)
    content = pygments.highlight(content, lexer, formatter)
    link = get_stylesheet()
    return RenderResult(content, assets={'css':[link]})


def get_stylesheet():
    return '<link rel="stylesheet" href="{static_url}/mfr_code_pygments/css/{theme}.css" />'\
        .format(static_url=core_config['STATIC_URL'], theme=module_config['PYGMENTS_THEME'])
