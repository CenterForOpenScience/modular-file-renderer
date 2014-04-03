"""Image renderer module."""

def render_img_tag(fp, src=None, alt=''):
    """A simple image tag renderer.

    :param str:
    """
    # Default src to the filename
    if src is None:
        src = fp.name
    return '<img src="/{src}" alt="{alt}" />'.format(src=src, alt=alt)
