"""A molecular renderer module """

import os
import mfr
from mfr.core import RenderResult, get_assets_from_list

# assets must be loaded in this order
JS_ASSETS = [
    'modernizr.js',
    'foundation-5.4.7.min.js',
    'gl-matrix.js',
    'core.js',
    'geom.js',
    'trace.js',
    'symmetry.js',
    'mol.js',
    'io.js',
    'vert-assoc.js',
    'buffer-allocators.js',
    'vertex-array-base.js',
    'indexed-vertex-array.js',
    'vertex-array.js',
    'chain-data.js',
    'geom-builders.js',
    'scene.js',
    'render.js',
    'shade.js',
    'cam.js',
    'shaders.js',
    'framebuffer.js',
    'slab.js',
    'animation.js',
    'viewer.js',
]

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'templates', 'pv.html')


def render_html(fp, src=None, **kwargs):
    """ A molecular renderer.

    :param fp: File pointer
    :param src: Path to source file
    :return: A RenderResult object containing html content and js assets
    """
    src = src or fp.name

    with open(TEMPLATE) as template:
        content = template.read().format(pdb_file='\'' + src + '\'')

    assets_uri_base = '{0}/mfr_pdb'.format(mfr.config['STATIC_URL'])

    assets = {
        'js': get_assets_from_list(assets_uri_base, 'js', JS_ASSETS)
    }

    return RenderResult(content, assets)
