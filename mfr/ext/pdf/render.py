"""PDF renderer module."""
from mfr.core import RenderResult
import os

import mfr

from mfr.core import RenderResult
from mako.lookup import TemplateLookup


TEMPLATE = TemplateLookup(
    directories=[os.path.join(os.path.dirname(__file__),
        'templates')]).get_template('viewer.mako')


def render_html(fp, src):
    """A simple pdf renderer.
    :param fp: File pointer
    :param src: Path to file
    :return: A RenderResult object containing html content and js assets for pdf rendering
    """
    base = '{0}/pdf'.format(mfr.config['ASSETS_URL'])

    content = TEMPLATE.render(base=base, url=src)
    return RenderResult(content)
