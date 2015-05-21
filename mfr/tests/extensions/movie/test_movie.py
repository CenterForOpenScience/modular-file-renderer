import pytest

from mfr.extensions.movie import MovieRenderer

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
    return MovieRenderer(url, file_path, assets_url, extension)


class TestMovie:

    def test_render_movie(self, provider):
        result = provider.render()
