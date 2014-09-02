# -*- coding: utf-8 -*-
import os.path
from IPython.nbformat import current as nbformat
from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter

from mfr import config as core_config, RenderResult


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
        nb = nbformat.reads_json(content)
    except ValueError:
        return RenderResult("Invalid json")

    # name, theme = get_metadata(nb)
    body = exporter.from_notebook_node(nb)[0]

    HERE = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(HERE, 'templates', 'ipynb.html')

    with open(filename) as template:
        content = template.read().format(
            body=body,
        )

    # TODO These come from nb viewer, but conflict with the page.
    assets = {
        'css':  get_stylesheets(
            "mfr_ipynb/css/pygments.css",
            # "mfr_ipynb/css/style.min.css",
            # "mfr_ipynb/css/theme/cdp_1.css",
            # "mfr_ipynb/css/theme/css_linalg.css",
            ),
    }

    return RenderResult(content, assets)


# Metadata not currently used
# def get_metadata(nb):
#     # notebook title
#     name = nb.get('metadata', {}).get('name', None) or "untitiled.ipynb"

#     if not name.endswith(".ipynb"):
#         name += ".ipynb"

#     css_theme = nb.get('metadata', {})\
#                   .get('_nbviewer', {})\
#                   .get('css', None)
#     if css_theme and not re.match('\w', css_theme):
#         css_theme = None

#     return name, css_theme


def get_stylesheets(*args):
    return [os.path.join(core_config['STATIC_URL'], path) for path in args]
