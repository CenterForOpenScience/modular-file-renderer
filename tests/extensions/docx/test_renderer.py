import os
import pytest

from pydocx.exceptions import MalformedDocxException

from mfr.core.provider import ProviderMetadata

from mfr.extensions.docx import DocxRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.docx', 'text/plain', '1234', 'http://wb.osf.io/file/test.docx?token=1234')


@pytest.fixture
def test_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.docx')


@pytest.fixture
def invalid_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.docx')


@pytest.fixture
def url():
    return 'http://osf.io/file/file.docx'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def renderer(metadata, test_file_path, url, assets_url, export_url):
    return DocxRenderer(metadata, test_file_path, url, assets_url, export_url)


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()



class TestDocxRenderer:

    def test_render_docx(self, renderer, url):
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer">' in body

    def test_render_docx_invalid(self, metadata, invalid_file_path, url, assets_url, export_url):
        renderer = DocxRenderer(metadata, invalid_file_path, url, assets_url, export_url)
        with pytest.raises(MalformedDocxException):
            renderer.render()

    def test_render_docx_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_docx_cache_result(self, renderer):
        assert renderer.cache_result is True
