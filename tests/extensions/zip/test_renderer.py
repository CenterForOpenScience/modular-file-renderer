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
def test_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.zip')


@pytest.fixture
def url():
    return 'http://osf.io/file/test.zip'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, test_file_path, url, assets_url, export_url):
    return ZipRenderer(metadata, test_file_path, url, assets_url, export_url)


class TestZipRenderer:

    def test_format_zip(self, renderer):

        with ZipFile(os.path.join(BASE, 'files', 'test.zip'), 'r') as zip_file:
            zip_string = renderer.format_zip(zip_file)
        assert 'test 1<br>__MACOSX/<br>__MACOSX/._test 1<br>test 2<br>__MACOSX/._test 2' == zip_string