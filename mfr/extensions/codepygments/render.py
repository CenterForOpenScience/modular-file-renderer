"""Code renderer module."""
import os
import pygments
import pygments.lexers
import pygments.lexers.special
import pygments.formatters
from pygments.util import ClassNotFound
from mako.lookup import TemplateLookup

from mfr.core import extension
#from mfr import Config as core_config

DEFAULT_LEXER = pygments.lexers.special.TextLexer

def render_html(fp, *args, **kwargs):
    """Generate an html representation of the file

    :param fp: File pointer
    :return: RenderResult object containing the content html and its assets
    """
    formatter = pygments.formatters.HtmlFormatter(cssclass='default.css')
    content = fp.read()
    try:
        lexer = pygments.lexers.guess_lexer_for_filename(fp.name, content)
    except ClassNotFound:
        lexer = DEFAULT_LEXER()
    content = pygments.highlight(content, lexer, formatter)
    assets = {"css": [get_stylesheet()]}
    print(assets)
    return content

def get_stylesheet():
    """Generate an html link to a stylesheet"""
    return "{static_url}/code_pygments/css/{theme}.css".format(
        static_url='/static/public/mfr/code_pygments/css/default.css',
        theme='default')


class CodePygmentsRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        with open(self.file_path) as fp:
            content = render_html(fp)
            return self.TEMPLATE.render(base=self.assets_url, color='default.css', body=content)

    @property
    def requires_file(self):
        return True
