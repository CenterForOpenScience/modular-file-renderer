import pytest

from mfr.extensions.image import ImageRenderer


@pytest.fixture
def url():
    return 'test_jpg.jpg'


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
    return ImageRenderer(url, file_path, assets_url, extension)

class TestImage:

    def test_render_image(self, provider):
        html = provider.render()
        assert html.equals('<img src="{test_jpg.jpg}" />')