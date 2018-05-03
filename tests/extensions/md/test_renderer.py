import os

import pytest

from mfr.core.provider import ProviderMetadata
from mfr.extensions.md import MdRenderer


@pytest.fixture
def provider_metadata():
    return ProviderMetadata('test', '.md', 'text/plain', '1234', 'http://wb.osf.io/file/test.md?token=1234')


@pytest.fixture
def test_md_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.md')


@pytest.fixture
def url():
    return 'http://osf.io/file/test.md'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def mock_renderer(provider_metadata, test_md_file_path, url, assets_url, export_url):
    return MdRenderer(provider_metadata, test_md_file_path, url, assets_url, export_url)


class TestMdRenderer:

    def test_render_md_file_required(self, mock_renderer):
        assert mock_renderer.file_required is True

    def test_render_md_cache_result(self, mock_renderer):
        assert mock_renderer.cache_result is True

    def test_render_md(self, mock_renderer):
        body = mock_renderer.render()
        assert mock_renderer.metadata.download_url in body
