"""PDF renderer module."""
from mfr.core import RenderResult
from mfr import config as core_config
import os


def get_assets():
    """Creates a dictionary of js and css assets"""

    static_dir = os.path.join('/static', 'mfr', 'mfr_pdf')

    js_files = [
        "pdf.js",
        "compatibility.js",
        "jquery.min.js",
    ]

    assets = {}
    jspath = os.path.join('{static}', 'js', '{fname}')
    assets['js'] = [jspath.format(static=static_dir, fname=fname)
                    for fname in js_files]

    return assets


def render_pdf(fp, src=None):
    """A simple pdf renderer.

    :param str:
    """
    src = src or fp.name

    HERE = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(HERE, 'templates', 'pdfpage.html')

    with open(filename) as template:
        content = template.read().format(
            url=src,
            STATIC_PATH=core_config['STATIC_URL']
        )

    return RenderResult(content, assets=get_assets())
