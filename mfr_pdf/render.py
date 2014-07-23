"""PDF renderer module."""
from mfr.core import RenderResult


def render_pdf_mako(fp, src=None, alt=''):
    """A simple pdf renderer.

    :param str:
    """
    # Default src to the filename
    if src is None:
        src = fp.name

    # content = '<img src="{src}" alt="{alt}" />'.format(src=src, alt=alt)
    content =
    return RenderResult(content)

