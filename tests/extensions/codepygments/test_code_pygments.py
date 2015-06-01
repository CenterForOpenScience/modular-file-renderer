import pytest

from mfr.extensions.codepygments import CodePygmentsRenderer


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
    return CodePygmentsRenderer(url, file_path, assets_url, extension)

class TestCodepygments:

    def test_render_codepygments(self, provider):
        html = provider.render()