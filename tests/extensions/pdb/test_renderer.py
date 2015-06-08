import pytest

from mfr.extensions.pdb import PdbRenderer


@pytest.fixture
def url():
    return 'http://osf.io/file/test.pdb'


@pytest.fixture
def download_url():
    return 'http://wb.osf.io/file/test.pdb?token=1234'


@pytest.fixture
def file_path():
    return '/tmp/test.pdb'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def extension():
    return '.pdb'


@pytest.fixture
def renderer(url, download_url, file_path, assets_url, extension):
    return PdbRenderer(url, download_url, file_path, assets_url, extension)


class TestPdbRenderer:

    def test_render_pdb(self, renderer):
        body = renderer.render()
        assert '<div id="mfrViewer"></div>' in body
