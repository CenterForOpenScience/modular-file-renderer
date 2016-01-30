import os
import pytest

from mfr.core.provider import ProviderMetadata

from mfr.extensions.ipynb import IpynbRenderer
from mfr.extensions.ipynb.exceptions import InvalidFormat


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.ipynb', 'text/plain', '1234', 'http://wb.osf.io/file/test.ipynb?token=1234')


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
def url():
    return 'http://osf.io/file/file.ipynb'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, test_file_path, url, assets_url, export_url):
    return IpynbRenderer(metadata, test_file_path, url, assets_url, export_url)


class TestIpynbRenderer:

    def test_render_ipynb(self, renderer, url):
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer mfr-ipynb-body">' in body

    def test_render_ipynb_no_metadata(self, metadata, no_metadata_file_path, url, assets_url, export_url):
        renderer = IpynbRenderer(metadata, no_metadata_file_path, url, assets_url, export_url)
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer mfr-ipynb-body">' in body

    def test_render_ipynb_invalid_json(self, metadata, invalid_json_file_path, url, assets_url, export_url):
        renderer = IpynbRenderer(metadata, invalid_json_file_path, url, assets_url, export_url)
        with pytest.raises(InvalidFormat):
            renderer.render()

    def test_render_docx_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_docx_cache_result(self, renderer):
        assert renderer.cache_result is True
