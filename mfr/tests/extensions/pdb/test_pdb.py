import pytest

from mfr.extensions.pdb import PdbRenderer


@pytest.fixture
def url():
    return 'http://www.cos.io/test.pdb'


@pytest.fixture
def file_path():
    return {}


@pytest.fixture
def assets_url():
    return 'insert path here'


@pytest.fixture
def extension():
    return {}


@pytest.fixture
def provider(url, file_path, assets_url, extension):
    return PdbRenderer(url, file_path, assets_url, extension)

class TestPdb:

    def test_render_pdb(self, provider):
        html = provider.render()


