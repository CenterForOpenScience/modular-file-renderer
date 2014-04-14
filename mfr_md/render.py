import markdown

def render_html(fp):
    #print(markdown.markdown(fp.read()))
    return(markdown.markdown(fp.read()))
