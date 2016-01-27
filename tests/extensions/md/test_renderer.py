import os
import pytest

from mfr.core.provider import ProviderMetadata
from mfr.extensions.md import MdRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.md', 'text/plain', '1234', 'http://wb.osf.io/file/test.md?token=1234')


@pytest.fixture
def test_md_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.md')


@pytest.fixture
def invalid_md_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.md')

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
def renderer(metadata, test_md_file_path, url, assets_url, export_url):
    return MdRenderer(metadata, test_md_file_path, url, assets_url, export_url)


class TestMdRenderer:

    def test_render_md_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_md_cache_result(self, renderer):
        assert renderer.cache_result is True

    def test_render_md(self, test_md_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.md', 'text/plain', '1234', 'http://wb.osf.io/file/test.md?token=1234')
        renderer = MdRenderer(metadata, test_md_file_path, url, assets_url, export_url)
        body = renderer.render()
        assert '<ul>\n<li>one</li>\n<li>two</li>\n</ul>' in body

