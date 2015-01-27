"""PDF renderer module."""
import os

import mfr

from mfr.core import RenderResult, get_assets_from_list
from mfr import config as core_config

JS_ASSETS = [
    "pdf.js",
    "compatibility.js",
    "jquery.min.js",
]


HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'templates', 'pdfpage.html')


def render_pdf(fp, src=None):
    """A simple pdf renderer.

    :param str:
    """
    src = src or fp.name

    assets_uri_base = '{0}/mfr_pdf'.format(mfr.config['STATIC_URL'])

    assets = {
        'js': get_assets_from_list(assets_uri_base, 'js', JS_ASSETS)
    }

    with open(TEMPLATE) as template:
        content = template.read().format(
            url=src,
            STATIC_PATH=core_config['STATIC_URL']
        )

    return RenderResult(content, assets=assets)
