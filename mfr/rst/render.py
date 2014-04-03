"""TEMPLATE renderer module."""

def render_TEMPLATE_tag(fp, src=None, alt=''):
    """A simple TEMPLATE tag renderer.

    :param str:
    """
    # Default src to the filename
    if src is None:
        src = fp.name
    return '<img src="{src}" alt="{alt}" />'.format(src=src, alt=alt)
