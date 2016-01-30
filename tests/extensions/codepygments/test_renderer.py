import os
import pytest

from mfr.core.provider import ProviderMetadata

from mfr.extensions.codepygments import CodePygmentsRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.xml', 'text/plain', '1234', 'http://wb.osf.io/file/good.xml?token=1234')


@pytest.fixture
def test_file_path():
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.xml')


@pytest.fixture
def invalid_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.xml')


@pytest.fixture
def url():
    return 'http://osf.io/file/good.xml'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def extension():
    return '.mp3'


@pytest.fixture
def renderer(metadata, test_file_path, url, assets_url, export_url):
    return CodePygmentsRenderer(metadata, test_file_path, url, assets_url, export_url)


class TestCodePygmentsRenderer:

    def test_render_codepygments(self, renderer):
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer">' in body

    def test_render_codepygments_invalid(self, metadata, invalid_file_path, url, assets_url, export_url):
        # additional decoding logic was added in the renderer, thus this should not render as text.
        renderer = CodePygmentsRenderer(metadata, invalid_file_path, url, assets_url, export_url)
        renderer.render()

    def test_render_codepygments_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_codepygments_cache_result(self, renderer):
        assert renderer.cache_result is True
