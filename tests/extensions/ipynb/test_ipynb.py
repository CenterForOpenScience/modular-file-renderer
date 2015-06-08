import os
import pytest

from mfr.extensions.ipynb import IpynbRenderer
from mfr.extensions.ipynb.exceptions import InvalidFormat

@pytest.fixture
def url():
    return 'http://osf.io/file/file.ipynb'


@pytest.fixture
def download_url():
    return 'http://wb.osf.io/file/file.ipynb?token=1234'


@pytest.fixture
def test_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.ipynb')


@pytest.fixture
def no_metadata_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'no_metadata.ipynb')


@pytest.fixture
def invalid_json_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid_json.ipynb')


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def extension():
    return '.ipynb'


@pytest.fixture
def renderer(url, download_url, test_file_path, assets_url, extension):
    return IpynbRenderer(url, download_url, test_file_path, assets_url, extension)


class TestIpynbRenderer:

    def test_render_ipynb(self, renderer, url):
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer mfr-ipynb-body">' in body

    def test_render_ipynb_no_metadata(self, url, download_url, no_metadata_file_path, assets_url, extension):
        renderer = IpynbRenderer(url, download_url, no_metadata_file_path, assets_url, extension)
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer mfr-ipynb-body">' in body

    def test_render_ipynb_invalid_json(self, url, download_url, invalid_json_file_path, assets_url, extension):
        renderer = IpynbRenderer(url, download_url, invalid_json_file_path, assets_url, extension)
        with pytest.raises(InvalidFormat):
            renderer.render()

    def test_render_docx_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_docx_cache_result(self, renderer):
        assert renderer.cache_result is True
