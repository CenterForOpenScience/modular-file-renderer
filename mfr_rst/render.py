""" ReStructuredText renderer module """
from docutils.core import publish_parts
from mfr import RenderResult

def render_rst(fp, *args, **kwargs):
    """A simple reStructuredText renderer

    :param fp: File pointer
    :return: A RenderResult containing html content for rst rendering

    """
    htmlstring = publish_parts(fp.read(), writer_name='html')['html_body']
    return RenderResult(htmlstring)
