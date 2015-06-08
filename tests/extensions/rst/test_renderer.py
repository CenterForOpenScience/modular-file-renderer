import os
import pytest

from mfr.extensions.rst import RstRenderer


@pytest.fixture
def url():
    return 'http://osf.io/file/test.rst'


@pytest.fixture
def download_url():
    return 'http://wb.osf.io/file/test.rst?token=1234'


@pytest.fixture
def test_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.rst')


@pytest.fixture
def invalid_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.rst')


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def extension():
    return '.rst'


@pytest.fixture
def renderer(url, download_url, test_file_path, assets_url, extension):
    return RstRenderer(url, download_url, test_file_path, assets_url, extension)


class TestRstRenderer:

    def test_render_rst(self, renderer):
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer">' in body

    def test_render_rst_invalid(self, url, download_url, invalid_file_path, assets_url, extension):
        renderer = RstRenderer(url, download_url, invalid_file_path, assets_url, extension)
        with pytest.raises(UnicodeDecodeError):
            renderer.render()

    def test_render_rst_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_rst_cache_result(self, renderer):
        assert renderer.cache_result is True
