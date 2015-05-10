""" ReStructuredText renderer module """
from docutils.core import publish_parts
from mfr.core import extension

def render_rst(fp, *args, **kwargs):
    """A simple reStructuredText renderer

    :param fp: File pointer
    :return: A RenderResult containing html content for rst rendering

    """
    htmlstring = publish_parts(fp.read(), writer_name='html')['html_body']

class RstRenderer(extension.BaseRenderer):

    def render(self):
        return '<html>'