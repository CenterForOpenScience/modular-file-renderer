# -*- coding: utf-8 -*-
"""IPython NoteBook renderer module"""
import os
from mfr import config as core_config
from mfr import RenderResult
from mfr.core import get_assets_from_list
from IPython.nbformat import current as nbformat
from IPython.nbformat import reader as nbread
from IPython.nbformat.reader import NotJSONError
from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter


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
    """A renderer for IPython NoteBooks.

    :param file_pointer: File pointer
    :return: RenderResult object containing the content html and css assets
    """
    try:
        content = file_pointer.read()
        nb = nbformat.reads_json(content)
    except ValueError as e:
        return RenderResult("Invalid json: {0}".format(e))

    # name, theme = get_metadata(nb)
    body = exporter.from_notebook_node(nb)[0]

    with open(TEMPLATE) as template:
        content = template.read().format(
            body=body,
        )

    assets = get_assets()

    return RenderResult(content, assets)


def get_assets():
    assets_uri_base = '{0}/ipynb'.format(core_config['ASSETS_URL'])

    assets = {
        'css': get_assets_from_list(assets_uri_base, 'css', CSS_ASSETS)
    }

    return assets

# Metadata not currently used
def get_metadata(nb):
    # notebook title
    name = 'untitled'
    css_theme = None
    try:
        content = nb.read()
        nb = nbread.parse_json(content)
        try:
            name = nb['metadata']['name']
        except KeyError:
            pass
        try:
            css_theme = nb['metadata']['nbviewer']['css']
        except KeyError:
            pass
    except NotJSONError:
        return 'Unable to parse json', 'No metadata found'

    return name, css_theme
