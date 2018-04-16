import furl
import pytest
import re

from mfr.extensions.pdf import (settings,
                                PdfRenderer)
from mfr.core.provider import ProviderMetadata


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.pdf', 'text/plain', '1234',
                            'http://wb.osf.io/file/test.pdf?token=1234')

@pytest.fixture
def tif_metadata():
    return ProviderMetadata('test', '.tif', 'text/plain', '1234',
                            'http://wb.osf.io/file/test.tif?token=1234')

@pytest.fixture
def docx_metadata():
    return ProviderMetadata(
        'te\'st',
        '.docx',
        'text/plain',
        '1234',
        'http://mfr.osf.io/export?url=http://osf.io/file/te\'st.pdf'
    )

@pytest.fixture
def file_path():
    return '/tmp/test.pdf'

@pytest.fixture
def tif_file_path():
    return '/tmp/test.tif'

@pytest.fixture
def docx_file_path():
    return '/tmp/te\'st.docx'


@pytest.fixture
def url():
    return 'http://osf.io/file/te\'st.pdf'


@pytest.fixture
def tif_url():
    return 'http://osf.io/file/te\'st.tif'


@pytest.fixture
def docx_url():
    return 'http://osf.io/file/te\'st.tif'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=http://osf.io/file/te\'st.pdf'


@pytest.fixture
def renderer(metadata, file_path, url, assets_url, export_url):
    return PdfRenderer(metadata, file_path, url, assets_url, export_url)


@pytest.fixture
def tif_renderer(
    tif_metadata,
    tif_file_path,
    tif_url,
    assets_url,
    export_url
):
    return PdfRenderer(tif_metadata, tif_file_path, tif_url, assets_url, export_url)


@pytest.fixture
def docx_renderer(
    docx_metadata,
    docx_file_path,
    docx_url,
    assets_url,
    export_url
):
    return PdfRenderer(
        docx_metadata,
        docx_file_path,
        docx_url,
        assets_url,
        export_url
    )


class TestPdfRenderer:

    def test_render_pdf(self, renderer, metadata, assets_url):
        body = renderer.render()
        assert '<base href="{}/{}/web/" target="_blank">'.format(assets_url, 'pdf') in body
        assert '<div id="viewer" class="pdfViewer"></div>' in body
        assert 'DEFAULT_URL = \'{}\''.format(metadata.download_url) in body

    def test_render_tif(self, tif_renderer, assets_url):
        exported_url = furl.furl(tif_renderer.export_url)
        exported_url.args['format'] = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE,
                                                            settings.EXPORT_TYPE)

        body = tif_renderer.render()
        assert '<base href="{}/{}/web/" target="_blank">'.format(assets_url, 'pdf') in body
        assert '<div id="viewer" class="pdfViewer"></div>' in body
        assert 'DEFAULT_URL = \'{}\''.format(exported_url.url) in body

    def test_render_docx(self, docx_renderer, assets_url):
        exported_url = furl.furl(docx_renderer.export_url)

        body = docx_renderer.render()
        assert '<base href="{}/{}/web/" target="_blank">'.format(assets_url, 'pdf') in body
        assert '<div id="viewer" class="pdfViewer"></div>' in body
        assert 'DEFAULT_URL = \'{}\''.format(re.sub(r'\'', '\\\'', exported_url.url)) in body

