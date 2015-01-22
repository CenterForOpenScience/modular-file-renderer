import markdown
from mfr import RenderResult

def render_html(fp, **kwargs):
    return RenderResult(markdown.markdown(fp.read()))
