import mfr_md
from mfr_md import render

def test_render_html(fakefile):
    fakefile.read.return_value = '# foo'
    assert render.render_html(fakefile) == '<h1>foo</h1>'
    fakefile.read.return_value = '_italic_'
    assert render.render_html(fakefile) == '<p><em>italic</em></p>'
    fakefile.read.return_value = '*italic*'
    assert render.render_html(fakefile) == '<p><em>italic</em></p>'
    
