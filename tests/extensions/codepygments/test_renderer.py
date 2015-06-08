import os
import pytest

from mfr.extensions.codepygments import CodePygmentsRenderer


@pytest.fixture
def url():
    return 'http://osf.io/file/good.xml'


@pytest.fixture
def download_url():
    return 'http://wb.osf.io/file/good.xml?token=1234'


@pytest.fixture
def test_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.xml')


@pytest.fixture
def invalid_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.xml')


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def extension():
    return '.mp3'


@pytest.fixture
def renderer(url, download_url, test_file_path, assets_url, extension):
    return CodePygmentsRenderer(url, download_url, test_file_path, assets_url, extension)


class TestCodePygmentsRenderer:

    def test_render_codepygments(self, renderer):
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer">' in body

    def test_render_codepygments_invalid(self, url, download_url, invalid_file_path, assets_url, extension):
        renderer = CodePygmentsRenderer(url, download_url, invalid_file_path, assets_url, extension)
        with pytest.raises(UnicodeDecodeError):
            renderer.render()

    def test_render_codepygments_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_codepygments_cache_result(self, renderer):
        assert renderer.cache_result is True
