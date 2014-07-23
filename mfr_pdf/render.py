"""PDF renderer module."""
from mfr.core import RenderResult
from mako.lookup import TemplateLookup
import PyPDF2

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

mako_lookup = TemplateLookup(
            directories=['/templates']
        )

def render_mako(fp, **kwargs):
    return mako_lookup.get_template(filename).render(**kwargs)


def render_pdf_mako(fp, **kwargs):
    url = kwargs['url']
    return render_mako(
        "pdfpage.mako",
        url=url,
        STATIC_PATH=self.STATIC_PATH,
    )
