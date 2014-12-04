import os
import mfr
from mfr.core import RenderResult, get_assets_from_list

# assets must be loaded in this order
JS_ASSETS = [
    'jquery-2.0.2.min.js',
    'modernizr.js',
    'foundation-5.4.7.min.js',
    'src/gl-matrix.js',
    'src/core.js',
    'src/geom.js',
    'src/trace.js',
    'src/symmetry.js',
    'src/mol.js',
    'src/io.js',
    'src/vert-assoc.js',
    'src/buffer-allocators.js',
    'src/vertex-array-base.js',
    'src/indexed-vertex-array.js',
    'src/vertex-array.js',
    'src/chain-data.js',
    'src/geom-builders.js',
    'src/scene.js',
    'src/render.js',
    'src/shade.js',
    'src/cam.js',
    'src/shaders.js',
    'src/framebuffer.js',
    'src/slab.js',
    'src/animation.js',
    'src/viewer.js',    
] 

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'templates', 'pv.html')


def render_html(fp, src=None, **kwargs):

    src = src or fp.name

    with open(TEMPLATE) as template:
        content = template.read().format(pdb_file=  '\'' + src + '\'')

    assets_uri_base = '{0}/mfr_pdb'.format(mfr.config['STATIC_URL'])

    assets = {
        'js': get_assets_from_list(assets_uri_base, 'js', JS_ASSETS)
    }

    return RenderResult(content, assets)
