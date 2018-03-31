import os
import re
import json
from zipfile import ZipFile

import pytest

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
def zip_file_tree():
    return ZipFile(os.path.join(BASE, 'files', 'test-tree.zip'), 'r')


@pytest.fixture
def zip_empty_file():
    return ZipFile(os.path.join(BASE, 'files', 'empty.zip'), 'r')


@pytest.fixture
def test_file_path():
    return os.path.join(BASE, 'files', 'test.zip')


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


@pytest.fixture
def file_tree():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures/fixtures.json'), 'r') as fp:
        return json.load(fp)['file_tree']


class TestZipRenderer:

    def test_render(self, renderer):
        body = renderer.render()

    def test_filelist_to_tree(self, renderer, zip_file_tree, file_tree):

        files = [file for file in zip_file_tree.filelist if not file.filename.startswith('__MACOSX')]

        actual = renderer.filelist_to_tree(files)
        assert actual == file_tree

