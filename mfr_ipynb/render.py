# -*- coding: utf-8 -*-
import re
import os.path
from IPython.nbformat import current as nbformat
from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter
from mako.lookup import TemplateLookup

c = Config()
c.HTMLExporter.template_file = 'basic'
c.NbconvertApp.fileext = 'html'
c.CSSHTMLHeaderTransformer.enabled = False
c.Exporter.filters = {'strip_files_prefix': lambda s: s} #don't strip the files prefix
exporter = HTMLExporter(config=c)

STATIC_PATH = '/static'
DIR_PATH = '/home/pfan/modular-file-renderer/mfr_ipynb'

class NbFormatError(Exception):
    pass



def render_html(file_pointer, **kwargs):
    content = file_pointer.read()
    nb = parse_json(content)
    name, theme = get_metadata(nb)
    body = exporter.from_notebook_node(nb)[0]
    return render_mako(
            template_name="ipynb.mako",
            body=body,
            file_name=name,
            css_theme=theme,
            mathjax_conf=None
        )


def parse_json(content):
    try:
        nb = nbformat.reads_json(content)
    except ValueError:
        raise NbFormatError('Error reading json notebook')
    return nb


def get_metadata(nb):
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

def render_mako(template_name, css_theme, file_name, body, mathjax_conf, **kwargs):
    mako_lookup = TemplateLookup(directories=['/home/pfan/modular-file-renderer/mfr_ipynb/templates'])
    return mako_lookup.get_template(template_name).render(STATIC_PATH='/home/pfan/modular-file-renderer/mfr_ipynb/static', body=body, file_name=file_name, css_theme=css_theme, mathjax_conf=None)
