import markdown

def render_html(fp, **kwargs):
    return(markdown.markdown(fp.read()))
