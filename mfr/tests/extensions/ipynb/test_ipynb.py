import pytest

from mfr.extensions.ipynb import IpynbRenderer


@pytest.fixture
def url():
    return {}


@pytest.fixture
def file_path():
    return {}


@pytest.fixture
def assets_url():
    return {}


@pytest.fixture
def extension():
    return {}


@pytest.fixture
def provider(url, file_path, assets_url, extension):
    return IpynbRenderer(url, file_path, assets_url, extension)

class TestIpynb:

    def test_render_ipynb(self, provider):
        html = provider.render()
