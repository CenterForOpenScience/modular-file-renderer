import pytest

from mfr.extensions.pdf import PdfRenderer


@pytest.fixture
def url():
    return 'http://osf.io/file/test.pdf'


@pytest.fixture
def download_url():
    return 'http://wb.osf.io/file/test.pdf?token=1234'


@pytest.fixture
def file_path():
    return '/tmp/test.pdf'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def extension():
    return '.pdf'


@pytest.fixture
def renderer(url, download_url, file_path, assets_url, extension):
    return PdfRenderer(url, download_url, file_path, assets_url, extension)


class TestPdfRenderer:

    def test_render_pdf(self, renderer, download_url, assets_url):
        body = renderer.render()
        assert '<base href="{}/{}/web/">'.format(assets_url, 'pdf') in body
        assert '<div id="viewer" class="pdfViewer"></div>' in body
        assert 'DEFAULT_URL = \'{}\''.format(download_url) in body
