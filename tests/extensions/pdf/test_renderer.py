import pytest

from mfr.core.provider import ProviderMetadata

from mfr.extensions.pdf import PdfRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.pdf', 'text/plain', '1234', 'http://wb.osf.io/file/test.pdf?token=1234')


@pytest.fixture
def file_path():
    return '/tmp/test.pdf'


@pytest.fixture
def url():
    return 'http://osf.io/file/test.pdf'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, file_path, url, assets_url, export_url):
    return PdfRenderer(metadata, file_path, url, assets_url, export_url)


class TestPdfRenderer:

    def test_render_pdf(self, renderer, metadata, assets_url):
        body = renderer.render()
        assert '<base href="{}/{}/web/" target="_blank">'.format(assets_url, 'pdf') in body
        assert '<div id="viewer" class="pdfViewer"></div>' in body
        assert 'DEFAULT_URL = \'{}\''.format(metadata.download_url) in body
