import pytest

from mfr.extensions.rst import RstRenderer


@pytest.fixture
def url():
    return {}


@pytest.fixture
def file_path():
    return 'test.rst'


@pytest.fixture
def assets_url():
    return {}


@pytest.fixture
def extension():
    return {}


@pytest.fixture
def provider(url, file_path, assets_url, extension):
    return RstRenderer(url, file_path, assets_url, extension)

class TestRst:

    def test_render_rst(self, provider):
        html = provider.render()