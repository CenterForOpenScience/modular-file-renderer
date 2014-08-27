# -*- coding: utf-8 -*-
import os
import shutil

import pytest
import mock

from mfr import core
from mfr.exceptions import ConfigurationError, MFRException
from test_mfr.fakemodule import Handler as TestHandler


HERE = os.path.abspath(os.path.dirname(__file__))


def teardown_function(testfunc):
    core.reset_config()


def assert_file_exists(path, msg='File does not exist'):
    assert os.path.exists(path) is True, msg

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

def test_register_filehandler():
    core.register_filehandler(FakeHandler)
    assert FakeHandler in core.get_registry()


def test_register_filehandlers():
    core.register_filehandlers([FakeHandler, TestHandler])
    assert FakeHandler in core.get_registry()
    assert TestHandler in core.get_registry()


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


def test_render_raises_mfr_exception_if_renderer_not_found(fakefile):
    handler = FakeHandler()
    with pytest.raises(MFRException):
        handler.render(fakefile, renderer='notfound')


def test_export_raises_mfr_exception_if_exporter_not_found(fakefile):
    handler = FakeHandler()
    with pytest.raises(MFRException):
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
    core.register_filehandler(FakeHandler)
    core.render(fakefile, handler=FakeHandler())
    assert FakeHandler.renderers['html'].called


def test_error_raised_if_renderer_not_found(fakefile):
    with pytest.raises(MFRException):
        core.render(fakefile, handler=None)


def test_detect_returns_a_single_handler_class_by_default(fakefile):
    core.register_filehandler(FakeHandler)
    handler = core.detect(fakefile)
    assert isinstance(handler, FakeHandler)


def test_detect_can_return_instances(fakefile):
    core.register_filehandler(FakeHandler)
    handlers = core.detect(fakefile, many=True, instance=True)
    assert isinstance(handlers[0], FakeHandler)


def test_detect_many(fakefile):
    core.register_filehandler(FakeHandler)
    handlers = core.detect(fakefile, many=True)
    assert isinstance(handlers, list)
    assert isinstance(handlers[0], FakeHandler)


def test_detect_single(fakefile):
    core.register_filehandler(FakeHandler)
    handler = core.detect(fakefile, many=False)
    assert isinstance(handler, FakeHandler)


def test_detect_single_returns_none_if_no_handler_found(fakefile):
    core.clear_registry()
    assert core.detect(fakefile, many=False) is None


def test_detect_many_returns_empty_list_if_no_handler_found(fakefile):
    core.clear_registry()
    assert core.detect(fakefile, many=True) == []


def test_render_detects_filetype_if_no_handler_given(fakefile):
    core.register_filehandler(FakeHandler)
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


def test_get_dir_for_class():
    class Foo:
        pass
    assert core._get_dir_for_class(Foo) == os.path.abspath(
        os.path.dirname(__file__)
    )


def test_get_static_url_for_handler():
    core.config.update({
        'STATIC_URL': '/static'
    })
    url = core.get_static_url_for_handler(TestHandler)
    assert url == '/static/fakemodule'


def test_get_static_path_for_handler_from_class_var():
    class MyHandler(core.FileHandler):
        STATIC_PATH = 'foo/bar/static/'

    assert core.get_static_path_for_handler(MyHandler) == MyHandler.STATIC_PATH


def test_collect_static():
    core.register_filehandler(TestHandler)
    dest = os.path.join(HERE, 'static')
    core.collect_static(dest=dest)
    expected1 = os.path.join(HERE, 'static', 'fakemodule', 'fakestyle.css')
    assert_file_exists(expected1)
    # clean up
    shutil.rmtree(dest)


def test_collect_static_uses_configuration_value():
    core.register_filehandler(TestHandler)
    core.config['STATIC_FOLDER'] = os.path.join(HERE, 'static')
    core.collect_static()
    expected1 = os.path.join(HERE, 'static', 'fakemodule', 'fakestyle.css')
    assert_file_exists(expected1)
    shutil.rmtree(core.config['STATIC_FOLDER'])


def test_collect_static_raises_error_if_no_destination():
    with pytest.raises(ConfigurationError):
        core.collect_static()

STATIC_PATH = '/my/static/path'


def test_config_from_file():
    core.config.from_pyfile(__file__)
    assert core.config['STATIC_PATH'] == STATIC_PATH


def test_get_registry():
    core.register_filehandler(TestHandler)
    assert TestHandler in core.get_registry()


def test_registering_handlers_with_config():
    class FakeConfig:
        HANDLERS = [FakeHandler, TestHandler]
    core.config.from_object(FakeConfig)
    assert FakeHandler in core.get_registry()


def test_include_static_defaults_to_false():
    assert core.config['INCLUDE_STATIC'] is False


def test_get_namespace_defaults_to_module_name():
    assert core.get_namespace(TestHandler) == 'fakemodule'


def test_get_namespace_for_class_that_defines_namespace_var():
    class FooHandler(core.FileHandler):
        namespace = 'foonamespace'

    assert core.get_namespace(FooHandler) == 'foonamespace'


def test_iterstatic_folder():
    handler = TestHandler()
    assets = list(handler.iterstatic(url=False))
    assert os.path.abspath(
        os.path.join(HERE, 'fakemodule', 'static', 'fakestyle.css')) in assets
    assert len(assets) == 3


def test_iterstatic_url():
    core.config.update({
        'STATIC_URL': '/static'
    })
    handler = TestHandler()
    assets = list(handler.iterstatic(url=True))
    assert len(assets) == 3
    assert os.path.join('/static', 'fakemodule', 'fakestyle.css') in assets
    assert os.path.join('/static', 'fakemodule', 'fakejs', 'fakescript.js') in assets


def test_get_assets():
    core.config.update({
        'STATIC_URL': '/static'
    })
    handler = TestHandler()
    assets = handler.get_assets()
    assert assets['css'] == ['/static/fakemodule/fakestyle.css']
    assert assets['js'] == ['/static/fakemodule/fakejs/fakescript.js']
    assert assets['_'] == ['/static/fakemodule/noextfile']


def test_get_assets_with_extension():
    core.config.update({
        'STATIC_URL': '/static'
    })
    handler = TestHandler()
    css_assets = handler.get_assets('css')
    assert isinstance(css_assets, list)
    assert css_assets == ['/static/fakemodule/fakestyle.css']


def test_get_assets_returns_key_error_if_static_url_not_configured():
    handler = TestHandler()
    with pytest.raises(KeyError) as excinfo:
        handler.get_assets()
    assert 'STATIC_URL is not configured' in str(excinfo)


def test_get_assets_from_list():
    js_files = ["test_file.js"]
    asset_uri_base = "/server/here/"
    js_assets = core.get_assets_from_list(asset_uri_base, 'js', js_files)
    assert js_assets == ["/server/here/js/test_file.js"]


def test_get_assets_from_list_excludes_EXCLUDE_LIBS():
    core.config['EXCLUDE_LIBS'] = ["not_this_one.css"]
    asset_uri_base = "/server/here/"
    css_files = ["this_one.css", "not_this_one.css"]
    css_assets = core.get_assets_from_list(asset_uri_base, 'css', css_files)
    assert len(css_assets) == 1
    assert "not_this_one.css" not in css_assets
