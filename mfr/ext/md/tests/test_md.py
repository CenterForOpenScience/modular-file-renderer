from mfr.ext.md import Handler, render
from mock import MagicMock

def test_render_html():
    fakefile = MagicMock()
    fakefile.read.return_value = '# foo'
    assert render.render_html(fakefile).content == '<h1>foo</h1>'
    fakefile.read.return_value = '_italic_'
    assert render.render_html(fakefile).content == '<p><em>italic</em></p>'
    fakefile.read.return_value = '*italic*'
    assert render.render_html(fakefile).content == '<p><em>italic</em></p>'
    fakefile.read.return_value = '''
* one
* two'''
    assert render.render_html(fakefile).content == '''<ul>
<li>one</li>
<li>two</li>
</ul>'''
        
def test_detect(fakefile):
    test_handler=Handler()
    fakefile.name='file.notmd'
    assert test_handler.detect(fakefile) is False
    fakefile.name='file.md'
    assert test_handler.detect(fakefile) is True
    fakefile.name='file.markdown'
    assert test_handler.detect(fakefile) is True
