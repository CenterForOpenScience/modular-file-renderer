""" RST renderer module """
from docutils.core import publish_parts

def render_html(fp, *args, **kwargs):
    htmlstring = publish_parts(fp.read(), writer_name='html')['html_body']
    return htmlstring
