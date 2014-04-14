from mfr_md import render, Handler
from mfr.core import FileHandler

def test_render_html(fakefile):
    fakefile.read.return_value = '# foo'
    assert render.render_html(fakefile) == '<h1>foo</h1>'
    fakefile.read.return_value = '_italic_'
    assert render.render_html(fakefile) == '<p><em>italic</em></p>'
    fakefile.read.return_value = '*italic*'
    assert render.render_html(fakefile) == '<p><em>italic</em></p>'
    fakefile.read.return_value = '''
* one
* two'''
    assert render.render_html(fakefile) == '''<ul>
<li>one</li>
<li>two</li>
</ul>'''
        
def test_handler(fakefile):
    testHandler=Handler()
    fakefile.name='file.notmd'
    assert testHandler.detect(fakefile) == False
    fakefile.name='file.md'
    assert testHandler.detect(fakefile) == True
    fakefile.name='file.markdown'
    assert testHandler.detect(fakefile) == True

