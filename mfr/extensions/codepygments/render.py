"""Code renderer module."""
import pygments
import pygments.lexers
import pygments.lexers.special
import pygments.formatters
from pygments.util import ClassNotFound

from mfr.core import extension
#from mfr import config as core_config

DEFAULT_LEXER = pygments.lexers.special.TextLexer

def render_html(fp, *args, **kwargs):
    """Generate an html representation of the file

    :param fp: File pointer
    :return: RenderResult object containing the content html and its assets
    """
    formatter = pygments.formatters.HtmlFormatter(cssclass='codehilite')
    content = fp.read()
    try:
        lexer = pygments.lexers.guess_lexer_for_filename(fp.name, content)
    except ClassNotFound:
        lexer = DEFAULT_LEXER()
    content = pygments.highlight(content, lexer, formatter)
   # assets = {"css": [get_stylesheet()]}
    return content


def get_stylesheet():
    """Generate an html link to a stylesheet"""
    pass
    #return "{static_url}/code_pygments/css/{theme}.css".format(
    #    static_url=core_config['ASSETS_URL'],
    #    theme=module_config['PYGMENTS_THEME'])

class CodePygmentsRenderer(extension.BaseRenderer):

    def render(self):
        with open(self.file_path) as fp:
            return render_html(fp)

    @property
    def requires_file(self):
        return True
