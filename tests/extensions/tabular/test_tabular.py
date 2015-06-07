import pytest

from mfr.extensions.tabular import TabularRenderer


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
    return TabularRenderer(url, file_path, assets_url, extension)

class TestTabular:

    def test_render_tabular(self, provider):
        html = provider.render()