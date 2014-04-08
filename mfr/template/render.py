"""TEMPLATE renderer module."""


def render_html(fp, *args, **kwargs):
    """A simple TEMPLATE renderer. Takes file pointer and returns html

    :param str:
    """
    html = fp.read()
    return html
