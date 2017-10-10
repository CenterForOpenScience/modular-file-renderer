import os
import re
from zipfile import ZipFile

import pytest
from bs4 import BeautifulSoup

from mfr.core.provider import ProviderMetadata
from mfr.extensions.zip import ZipRenderer


BASE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def metadata():
    return ProviderMetadata('test',
                            '.zip',
                            'text/plain',
                            '1234',
                            'http://wb.osf.io/file/test.zip?token=1234')

@pytest.fixture
def zip_file():
    return ZipFile(os.path.join(BASE, 'files', 'test.zip'), 'r')


@pytest.fixture
def zip_empty_file():
    return ZipFile(os.path.join(BASE, 'files', 'empty.zip'), 'r')


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
def export_url(url):
    return 'http://mfr.osf.io/export?url=' + url


@pytest.fixture
def renderer(metadata, test_file_path, url, assets_url, export_url):
    return ZipRenderer(metadata, test_file_path, url, assets_url, export_url)



def remove_whitespace(str):
    str = re.sub('\n*', '', str)
    return re.sub(r'\ {2,}', '', str)


class TestZipRenderer:

    def test_render(self, renderer):
        body = renderer.render()
        parsed_html = BeautifulSoup(body)
        rows = parsed_html.findChildren('table')[0].findChildren(['tr'])

        name = rows[2].findChildren('td')[0].get_text().strip()
        assert 'test/test 1' == name

        date_modified = rows[2].findChildren('td')[1].get_text().strip()
        assert '2017-03-02 16:22:14' == date_modified

        size = rows[2].findChildren('td')[2].get_text().strip()
        assert '15B' == size

        # non-expanded zip file should have no children
        name = rows[4].findChildren('td')[0].get_text().strip()
        assert 'test/zip file which is not expanded.zip' == name
        assert body.count('zip file which is not expanded.zip') == 1

        size = rows[4].findChildren('td')[2].get_text().strip()
        assert '1.8KB' == size  # formatting of larger byte sizes

        # hidden files should be hidden
        assert body.count('__MACOSX') == 0

    def test_format_zip(self, renderer, zip_file):
        zip_string = renderer.format_zip(zip_file)

        parsed_html = BeautifulSoup(zip_string)
        rows = parsed_html.findChildren('table')[0].findChildren(['tr'])

        name = rows[2].findChildren('td')[0].get_text().strip()
        assert 'test/test 1' == name

        name = rows[3].findChildren('td')[0].get_text().strip()
        assert 'test/test 2' == name

    def test_format_zip_empty(self, renderer, zip_empty_file):
        zip_string = renderer.format_zip(zip_empty_file)

        assert zip_string == 'This zip file is empty.'

    def test_non_zip_file(self, renderer):
        zip_string = renderer.format_zip(b'')

        assert zip_string == 'This is not a valid zip file.'
