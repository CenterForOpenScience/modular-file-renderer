import pytest

from mfr.core.provider import ProviderMetadata

from mfr.extensions.pdb import PdbRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.pdb', 'text/plain', '1234', 'http://wb.osf.io/file/test.pdb?token=1234')


@pytest.fixture
def file_path():
    return '/tmp/test.pdb'


@pytest.fixture
def url():
    return 'http://osf.io/file/test.pdb'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, file_path, url, assets_url, export_url):
    return PdbRenderer(metadata, file_path, url, assets_url, export_url)


class TestPdbRenderer:

    def test_render_pdb(self, renderer):
        body = renderer.render()
        assert '<div id="mfrViewer"></div>' in body
