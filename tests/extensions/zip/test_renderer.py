import os
import pytest
from zipfile import ZipFile

from mfr.core.provider import ProviderMetadata

from mfr.extensions.zip import ZipRenderer

BASE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.zip', 'text/plain', '1234', 'http://wb.osf.io/file/test.zip?token=1234')

@pytest.fixture
def zip_file():
    return ZipFile(os.path.join(BASE, 'files', 'test.zip'), 'r')


@pytest.fixture
def test_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.zip')

@pytest.fixture
def test_render_body():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test_render_body.html'), 'r') as fp:
        return fp.read()


@pytest.fixture
def url():
    return 'http://osf.io/file/test.zip'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url(url):
    return 'http://mfr.osf.io/export?url=' + url


@pytest.fixture
def renderer(metadata, test_file_path, url, assets_url, export_url):
    return ZipRenderer(metadata, test_file_path, url, assets_url, export_url)


class TestZipRenderer:

    def test_render(self, renderer):
        body = renderer.render()

        assert '<td>test 2' in body and '<td>test 1' in body

    def test_format_zip(self, renderer, zip_file):
        zip_string = renderer.format_zip(zip_file)

        assert '<td>test 2' in zip_string and '<td>test 1' in zip_string
