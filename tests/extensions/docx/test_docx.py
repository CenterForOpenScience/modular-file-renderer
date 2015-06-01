import pytest

from mfr.extensions.docx import DocxRenderer

@pytest.fixture
def url():
    return {}


@pytest.fixture
def file_path():
    return 'test.docx'


@pytest.fixture
def assets_url():
    return {}


@pytest.fixture
def extension():
    return {}


@pytest.fixture
def provider(url, file_path, assets_url, extension):
    return DocxRenderer(url, file_path, assets_url, extension)


class TestDocx:

    def test_render_docx(self, provider):
        result = provider.render()

