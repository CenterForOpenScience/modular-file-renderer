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

def render_html(fp, ext, *args, **kwargs):
    """Generate an html representation of the file

    :param fp: File pointer
    :return: RenderResult object containing the content html and its assets
    """
    formatter = pygments.formatters.HtmlFormatter(cssclass='codehilite')
    content = fp.read()
    try:
        lexer = pygments.lexers.guess_lexer_for_filename(ext, content)
    except ClassNotFound:
        lexer = DEFAULT_LEXER()
    content = pygments.highlight(content, lexer, formatter)
    print(repr(content))
    return content


class CodePygmentsRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        with open(self.file_path) as fp:
            content = render_html(fp, self.ext)
            return self.TEMPLATE.render(base=self.assets_url, color='default.css', body=content)

    @property
    def requires_file(self):
        return True
