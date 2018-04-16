import os
import json
from zipfile import ZipFile

import pytest

from mfr.extensions.zip import ZipRenderer
from mfr.core.provider import ProviderMetadata

BASE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def test_file():
    return ZipFile(os.path.join(BASE, 'files', 'zip-test.zip'), 'r')


@pytest.fixture
def empty_file():
    return ZipFile(os.path.join(BASE, 'files', 'zip-empty.zip'), 'r')


@pytest.fixture
def test_file_path():
    return os.path.join(BASE, 'files', 'zip-test.zip')


@pytest.fixture
def test_file_path():
    return os.path.join(BASE, 'files', 'zip-empty.zip')


@pytest.fixture
def test_file_obj_name_list():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures/obj_list.json'), 'r') as fp:
        return json.load(fp)['test_file_list']


@pytest.fixture
def empty_file_obj_name_list():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures/obj_list.json'), 'r') as fp:
        return json.load(fp)['empty_file_list']


@pytest.fixture
def test_file_obj_list(test_file):
    return ZipRenderer.sanitize_obj_list(test_file.filelist)


@pytest.fixture
def test_file_obj_tree():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures/obj_tree.json'), 'r') as fp:
        return json.load(fp)['test_file_tree']


@pytest.fixture
def empty_file_obj_list(empty_file):
    return ZipRenderer.sanitize_obj_list(empty_file.filelist)


@pytest.fixture
def empty_file_obj_tree():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures/obj_tree.json'), 'r') as fp:
        return json.load(fp)['empty_file_tree']


@pytest.fixture
def file_metadata():
    return ProviderMetadata('test', '.zip', 'text/plain', '9876543210',
                            'https://test-wb.osf.io/file/test.zip?token=9876543210')


@pytest.fixture
def file_url():
    return 'http://osf.io/file/test.zip'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url(file_url):
    return 'http://mfr.osf.io/export?url=' + file_url


@pytest.fixture
def test_file_renderer(file_metadata, test_file_path, file_url, assets_url, export_url):
    return ZipRenderer(file_metadata, test_file_path, file_url, assets_url, export_url)


@pytest.fixture
def empty_file_renderer(file_metadata, test_file_path, file_url, assets_url, export_url):
    return ZipRenderer(file_metadata, test_file_path, file_url, assets_url, export_url)


@pytest.fixture
def test_file_obj_tree_partial():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures/obj_tree_partial.json'), 'r') as fp:
        return json.load(fp)['test_file_tree_partial'][0]


@pytest.fixture
def new_file_to_add(test_file_obj_tree_partial):
    return {
        'full_path': 'zip-test/file-no-ext',
        'path_segment': 'file-no-ext',
        'siblings': test_file_obj_tree_partial['children'][0]['children']
    }


@pytest.fixture
def new_folder_to_add(test_file_obj_tree_partial):
    return {
        'full_path': 'zip-test/folder-3/',
        'path_segment': 'folder-3',
        'siblings': test_file_obj_tree_partial['children'][0]['children']
    }


@pytest.fixture
def exiting_folder_to_skip(test_file_obj_tree_partial):
    return {
        'full_path': 'zip-test/folder-2/text-2.pdf',
        'path_segment': 'folder-2',
        'siblings': test_file_obj_tree_partial['children'][0]['children']
    }


@pytest.fixture
def existing_folder_to_update(test_file_obj_tree_partial):
    return {
        'full_path': 'zip-test/folder-1/',
        'path_segment': 'folder-1',
        'siblings': test_file_obj_tree_partial['children'][0]['children'],
        'icon': 'http://mfr.osf.io/assets/zip/img/folder.png',
        'data': {
            'size': '',
            'date': '2018-04-16 11:50:48'
        },
    }


@pytest.fixture
def obj_zip_info_to_update(test_file):
    for obj in test_file.filelist:
        if obj.filename == 'zip-test/folder-1/':
            return obj


class TestZipRenderer:

    # The rendered template HTML does not contain the actual data
    def test_render(self, test_file_renderer):
        test_file_renderer.render()

    def test_sanitize_obj_list(self, test_file, test_file_obj_name_list):
        obj_list = ZipRenderer.sanitize_obj_list(test_file.filelist)
        obj_name_list = [obj.filename for obj in obj_list if obj]
        assert sorted(obj_name_list) == sorted(test_file_obj_name_list)

    def test_sanitize_obj_list_empty(self, empty_file, empty_file_obj_name_list):
        obj_list = ZipRenderer.sanitize_obj_list(empty_file.filelist)
        obj_name_list = [obj.filename for obj in obj_list if obj]
        assert sorted(obj_name_list) == sorted(empty_file_obj_name_list)

    def test_find_node_among_siblings_return_node(self, exiting_folder_to_skip):
        segment = exiting_folder_to_skip['path_segment']
        siblings = exiting_folder_to_skip['siblings']
        assert ZipRenderer.find_node_among_siblings(segment, siblings)

    def test_find_node_among_siblings_return_none_file(self, new_file_to_add):
        segment = new_file_to_add['path_segment']
        siblings = new_file_to_add['siblings']
        assert not ZipRenderer.find_node_among_siblings(segment, siblings)

    def test_find_node_among_siblings_return_none_folder(self, new_folder_to_add):
        segment = new_folder_to_add['path_segment']
        siblings = new_folder_to_add['siblings']
        assert not ZipRenderer.find_node_among_siblings(segment, siblings)

    def test_icon_exists_true(self):
        assert ZipRenderer.icon_exists('png')

    def test_icon_exists_false(self):
        assert not ZipRenderer.icon_exists('mfr')

    def test_update_node_with_attributes(self, test_file_renderer, obj_zip_info_to_update,
                                         existing_folder_to_update):
        segment = existing_folder_to_update['path_segment']
        siblings = existing_folder_to_update['siblings']
        node_to_update = ZipRenderer.find_node_among_siblings(segment, siblings)
        assert not node_to_update.get('data', None) and not node_to_update.get('icon', None)
        test_file_renderer.update_node_with_attributes(node_to_update, obj_zip_info_to_update)
        assert node_to_update.get('data', {}) == existing_folder_to_update['data']
        assert node_to_update.get('icon', {}) == existing_folder_to_update['icon']

    def test_obj_list_to_tree(self, test_file_obj_list, test_file_renderer, test_file_obj_tree):
        obj_tree = test_file_renderer.obj_list_to_tree(test_file_obj_list)
        assert obj_tree == test_file_obj_tree

    def test_obj_list_to_tree_empty(self, empty_file_obj_list, empty_file_renderer,
                                    empty_file_obj_tree):
        obj_tree = empty_file_renderer.obj_list_to_tree(empty_file_obj_list)
        assert obj_tree == empty_file_obj_tree
