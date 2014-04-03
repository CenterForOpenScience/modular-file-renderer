from docutils.core import publish_parts
""" RST renderer module """

def render_html(fp, src=None, alt=''):
    htmlstring = publish_parts(fp.read(), writer_name='html')['html_body']
    return htmlstring