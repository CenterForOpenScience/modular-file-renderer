# -*- coding: utf-8 -*-
import re
import os.path
from IPython.nbformat import current as nbformat
from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter
from mako.lookup import TemplateLookup

from mfr import config as core_config, RenderResult
from mfr.core import get_static_path_for_handler


c = Config()
c.HTMLExporter.template_file = 'basic'
c.NbconvertApp.fileext = 'html'
c.CSSHTMLHeaderTransformer.enabled = False

# don't strip the files prefix
c.Exporter.filters = {'strip_files_prefix': lambda s: s}
exporter = HTMLExporter(config=c)


def render_html(file_pointer, **kwargs):

    try:
        content = file_pointer.read()
        nb = parse_json(content)
    except ValueError:
        return RenderResult("Invalid json")

    name, theme = get_metadata(nb)
    body = exporter.from_notebook_node(nb)[0]

    content = render_mako(
        template_name="ipynb.mako",
        body=body,
        file_name=name,
        css_theme=theme,
        mathjax_conf=None
    )

    assets = {
        'css': get_stylesheets(
            "mfr_ipynb/css/pygments.css",
            "mfr_ipynb/css/style.min.css",
            "mfr_ipynb/css/theme/cdp_1.css")
    }

    return RenderResult(content, assets)


def parse_json(content):
    return nbformat.reads_json(content)


def get_metadata(nb):
    # notebook title
    name = nb.get('metadata', {}).get('name', None) or "untitiled.ipynb"

    if not name.endswith(".ipynb"):
        name += ".ipynb"

    css_theme = nb.get('metadata', {})\
                  .get('_nbviewer', {})\
                  .get('css', None)
    if css_theme and not re.match('\w', css_theme):
        css_theme = None

    return name, css_theme


def render_mako(template_name, css_theme, file_name, body, mathjax_conf, **kwargs):
    template_path = os.path.split(get_static_path_for_handler(render_html))[0]
    template_path = os.path.join(template_path, 'templates')
    mako_lookup = TemplateLookup(directories=[template_path])

    return mako_lookup.get_template(template_name).render(
        body=body,
        file_name=file_name,
        css_theme=css_theme,
        mathjax_conf=None
    )


def get_stylesheets(*args):
    return [os.path.join(core_config['STATIC_URL'], path) for path in args]
