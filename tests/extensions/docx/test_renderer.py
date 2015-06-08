import os
import pytest

from mfr.extensions.docx import DocxRenderer
from pydocx.exceptions import MalformedDocxException


@pytest.fixture
def url():
    return 'http://osf.io/file/file.docx'


@pytest.fixture
def download_url():
    return 'http://wb.osf.io/file/file.docx?token=1234'


@pytest.fixture
def test_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.docx')


@pytest.fixture
def invalid_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.docx')


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def extension():
    return '.docx'


@pytest.fixture
def renderer(url, download_url, test_file_path, assets_url, extension):
    return DocxRenderer(url, download_url, test_file_path, assets_url, extension)


class TestDocxRenderer:

    def test_render_docx(self, renderer, url):
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer">' in body

    def test_render_docx_invalid(self, url, download_url, invalid_file_path, assets_url, extension):
        renderer = DocxRenderer(url, download_url, invalid_file_path, assets_url, extension)
        with pytest.raises(MalformedDocxException):
            renderer.render()

    def test_render_docx_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_docx_cache_result(self, renderer):
        assert renderer.cache_result is True
