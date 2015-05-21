import pytest

from mfr.extensions.pdf import PdfRenderer

@pytest.fixture
def url():
    return 'files/test.pdf'


@pytest.fixture
def file_path():
    return {}


@pytest.fixture
def assets_url():
    return 'insert path'


@pytest.fixture
def extension():
    return {}


@pytest.fixture
def provider(url, file_path, assets_url, extension):
    return PdfRenderer(url, file_path, assets_url, extension)


class TestPdf:

    def test_render_pdf(self, provider):
        result = provider.render()
