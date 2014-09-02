"""Image renderer module."""
from mfr.core import RenderResult


def render_img_tag(fp, src=None, alt=''):
    """A simple image tag renderer.

    :param str:
    """
    # Default src to the filename
    src = src or fp.name

    content = '<img src="{src}" alt="{alt}" />'.format(src=src, alt=alt)
    return RenderResult(content)
