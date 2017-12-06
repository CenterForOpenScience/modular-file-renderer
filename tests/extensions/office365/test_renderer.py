from urllib import parse

import furl
import pytest

from mfr.core.provider import ProviderMetadata
from mfr.extensions.office365 import Office365Renderer
from mfr.extensions.office365 import settings as office365_settings


@pytest.fixture
def metadata():
    return ProviderMetadata(
        'test',
        '.pdf',
        'text/plain',
        '1234',
        'http://wb.osf.io/file/test.pdf?token=1234&public_file=1',
        is_public=True
    )


@pytest.fixture
def file_path():
    return '/tmp/test.docx'


@pytest.fixture
def url():
    return parse.quote('http://osf.io/file/test.pdf')


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, file_path, url, assets_url, export_url):
    return Office365Renderer(metadata, file_path, url, assets_url, export_url)


class TestOffice365Renderer:

    def test_render_pdf(self, renderer, metadata):
        download_url = furl.furl(metadata.download_url).set(query='')
        office_render_url = office365_settings.OFFICE_BASE_URL + parse.quote(download_url.url)
        body = renderer.render()
        assert '<iframe src={} frameborder=\'0\'></iframe>'.format(office_render_url) in body
