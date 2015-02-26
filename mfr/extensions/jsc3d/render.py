"""3D renderer module """
# Uses jsc3d: https://code.google.com/p/jsc3d/
import os
import mfr
from mfr.core import RenderResult, get_assets_from_list

JS_ASSETS = [
    'jsc3d.js',
    'jsc3d.webgl.js',
    'jsc3d.touch.js',
]

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'templates', '3d.html')


def render_html(fp, src=None, **kwargs):
    """ A 3D renderer.

    :param fp: File pointer
    :param src: Path to source file
    :return: A RenderResult object containing html content and js assets
    """
    src = src or fp.name

    with open(TEMPLATE) as template:
        content = template.read().format(jsc3d_file=src)

    assets = get_assets()

    return RenderResult(content, assets)


def get_assets():
    assets_uri_base = '{0}/jsc3d'.format(mfr.config['ASSETS_URL'])

    assets = {
        'js': get_assets_from_list(assets_uri_base, 'js', JS_ASSETS)
    }

    return assets
