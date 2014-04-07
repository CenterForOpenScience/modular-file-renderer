"""ipynb renderer module."""

import re
import os.path
from mako.lookup import TemplateLookup
from IPython.config import Config
# from IPython.nbconvert import export_python
from IPython.nbconvert.exporters import HTMLExporter
from IPython.nbformat import current as nbformat

from mfr import config

c = Config()
c.HTMLExporter.template_file = 'basic'
c.NbconvertApp.fileext = 'html'
c.CSSHTMLHeaderTransformer.enabled = False
c.Exporter.filters = {'strip_files_prefix': lambda s: s} #don't strip the files prefix
exporter = HTMLExporter(config=c)


template_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'templates'
    )
)

template_lookup = TemplateLookup(template_path)

def render_html(fp, src=None, alt=''):
    content = fp.read()
    nb = _parse_json(content)
    name, theme = _get_metadata(nb)
    body = exporter.from_notebook_node(nb)[0]
    return template_lookup.get_template('ipynb.mako').render(
        file_name=name, css_theme=theme, mathjax_conf=None,
        body=body, STATIC_PATH=config['STATIC_ROOT'],
    )

def _parse_json(content):
    try:
        nb = nbformat.reads_json(content)
    except ValueError:
        raise NbFormatError('Error reading json notebook')
    return nb

def _get_metadata(nb):
    # notebook title
    name = nb.get('metadata', {}).get('name', None)
    if not name:
        name = "untitled.ipynb"
    if not name.endswith(".ipynb"):
        name += ".ipynb"

    # css
    css_theme = nb.get('metadata', {})\
                  .get('_nbviewer', {})\
                  .get('css', None)
    if css_theme and not re.match('\w', css_theme):
        css_theme = None
    return name, css_theme

def NbFormatError(Exception):
    pass