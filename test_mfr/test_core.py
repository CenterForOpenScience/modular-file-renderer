# -*- coding: utf-8 -*-
import os

import pytest
import mock

from mfr import core


def teardown_function(testfunc):
    # clear the registry after each test
    core._registry = {}

##### Fixtures, etc. ######

class FakeHandler(core.FileHandler):
    """A fake handler class for testing."""
    # use mocks to spy on the behavior of `render` and `export`
    renderers = {'html': mock.Mock()}
    exporters = {'myformat': mock.Mock()}
    default_renderer = 'html'
    default_exporter = 'myformat'

    def detect(self, fp):
        return True


##### The tests #####

def test_register_filetype():
    # clear the registry
    core._registry = {}
    core.register_filehandler('fakefiles', FakeHandler)
    assert core._registry['fakefiles'] == FakeHandler

def test_render_uses_default_renderer(fakefile):
    handler = FakeHandler()
    # render called without renderer name specified
    handler.render(fakefile)
    # default renderer was called
    assert FakeHandler.renderers['html'].called

def test_export_uses_default_exporter(fakefile):
    handler = FakeHandler()
    handler.export(fakefile)
    assert FakeHandler.exporters['myformat'].called

def test_render_raises_value_error_if_renderer_not_found(fakefile):
    handler = FakeHandler()
    with pytest.raises(ValueError):
        handler.render(fakefile, renderer='notfound')

def test_export_raises_value_error_if_exporter_not_found(fakefile):
    handler = FakeHandler()
    with pytest.raises(ValueError):
        handler.export(fakefile, exporter='notfound')

def test_render_can_take_extra_params(fakefile):
    # fake render function with an extra parameter
    def fake_render(fp, source):
        return '<img src="{source}"></img>'.format(source=source)
    # fake image handler class
    class FakeImageHandler(core.FileHandler):
        renderers = {'html': fake_render}
    handler = FakeImageHandler()
    source = '/my/file/baz.png'
    result = handler.render(fakefile, source=source)
    assert result == fake_render(fakefile, source)

def test_export_can_take_extra_params(fakefile):
    def fake_export(fp, dialect):
        return '...markdown rendered with {0}...'.format(dialect)
    class FakeTextHandler(core.FileHandler):
        exporters = {'markdown': fake_export}
    handler = FakeTextHandler()
    exported = handler.export(fakefile, exporter='markdown', dialect='maraku')
    assert exported == fake_export(fakefile, dialect='maraku')

def test_detect_must_be_implemented(fakefile):
    # handler with no detect method
    class BadHandler(core.FileHandler):
        pass
    handler = BadHandler()
    with pytest.raises(NotImplementedError):
        handler.detect(fakefile)

def test_render(fakefile):
    core.register_filehandler('myhandler', FakeHandler)
    core.render(fakefile, handler='myhandler')
    assert FakeHandler.renderers['html'].called

def test_error_raised_if_renderer_not_found(fakefile):
    with pytest.raises(ValueError):
        core.render(fakefile, handler='notfound')

def test_detect_returns_a_handler_class(fakefile):
    core.register_filehandler('myhandler', FakeHandler)
    handler_cls = core.detect(fakefile)
    assert issubclass(handler_cls, FakeHandler)

def test_detect_can_return_instance(fakefile):
    core.register_filehandler('myhandler', FakeHandler)
    handler = core.detect(fakefile, instance=True)
    assert isinstance(handler, FakeHandler)

def test_detect_returns_false_if_no_handler_found(fakefile):
    core._registry = {}
    assert core.detect(fakefile) is False

def test_render_detects_filetype_if_no_handler_given(fakefile):
    core.register_filehandler('myhandler', FakeHandler)
    core.render(fakefile)
    assert FakeHandler.renderers['html'].called

def test_get_file_extension():
    assert core.get_file_extension('foo.txt') == '.txt'
    assert core.get_file_extension('foo.TXT') == '.txt'
    assert core.get_file_extension('foo/bar/baz.Mp3') == '.mp3'
    assert core.get_file_extension('foo') == ''

def test_error_raised_if_renderer_not_callable(fakefile):
    bad_renderer = 'badnewsbears'
    class BadHandler(core.FileHandler):
        renderers = {'html': bad_renderer}
    with pytest.raises(TypeError):
        handler = BadHandler()
        handler.render(fakefile, 'html')

def test_find_static():
    assert 0, 'finish me'

def test_get_dir_for_class():
    class Foo:
        pass
    assert core._get_dir_for_class(Foo) == os.path.abspath(os.path.dirname(__file__))

def test_get_static_path_for_handler_from_class_var():
    class MyHandler(core.FileHandler):
        STATIC_PATH = 'foo/bar/static/'

    assert core.get_static_path_for_handler(MyHandler) == MyHandler.STATIC_PATH
