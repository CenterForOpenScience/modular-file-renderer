# -*- coding: utf-8 -*-
import os.path

import mfr

from IPython.nbformat import current as nbformat
from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter

from mfr import config as core_config, RenderResult
from mfr.core import get_assets_from_list


HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'templates', 'ipynb.html')

# TODO These come from nb viewer, but conflict with the page.
CSS_ASSETS = [
    "pygments.css",
    # "style.min.css",
    # "theme/cdp_1.css",
    # "theme/css_linalg.css",
]

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

    with open(TEMPLATE) as template:
        content = template.read().format(
            body=body,
        )

    assets_uri_base = '{0}/mfr_ipynb'.format(mfr.config['STATIC_URL'])

    assets = {
        'css': get_assets_from_list(assets_uri_base, 'css', CSS_ASSETS)
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
