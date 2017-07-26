import os
import pytest

from xlrd.biffh import XLRDError

from mfr.core.provider import ProviderMetadata

from mfr.extensions.tabular import settings
from mfr.extensions.tabular import TabularRenderer
from mfr.extensions.tabular import exceptions

PATH = os.path.dirname(os.path.abspath(__file__))
BODY = '<div id="mfrGrid" style="min-height: {}px;">\n    </div>'.format(settings.TABLE_HEIGHT)


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.csv', 'text/plain', '1234',
                            'http://wb.osf.io/file/test.csv?token=1234')


@pytest.fixture
def test_csv_file_path():
    return os.path.join(PATH, 'files', 'test.csv')


@pytest.fixture
def invalid_csv_file_path():
    return os.path.join(PATH, 'files', 'invalid.csv')


@pytest.fixture
def test_tsv_file_path():
    return os.path.join(PATH, 'files', 'test.tsv')


@pytest.fixture
def invalid_tsv_file_path():
    return os.path.join(PATH, 'files', 'invalid.tsv')


@pytest.fixture
def test_xlsx_file_path():
    return os.path.join(PATH, 'files', 'test.xlsx')


@pytest.fixture
def invalid_xlsx_file_path():
    return os.path.join(PATH, 'files', 'invalid.xlsx')


@pytest.fixture
def invalid_mat73_file_path():
    return os.path.join(PATH, 'files', 'invalidVer73.mat')


@pytest.fixture
def invalid_mat70_file_path():
    return os.path.join(PATH, 'files', 'invalidVer70.mat')


@pytest.fixture
def test_mat73_file_path():
    return os.path.join(PATH, 'files', 'testVer73.mat')


@pytest.fixture
def test_mat70_file_path():
    return os.path.join(PATH, 'files', 'testVer70.mat')


@pytest.fixture
def url():
    return 'http://osf.io/file/test.csv'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, test_csv_file_path, url, assets_url, export_url):
    return TabularRenderer(metadata, test_csv_file_path, url, assets_url, export_url)


class TestTabularRenderer:

    def test_render_tabular_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_tabular_cache_result(self, renderer):
        assert renderer.cache_result is True


class TestTabularCsvRenderer:

    def test_render_tabular_csv(self, test_csv_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.csv', 'text/plain', '1234',
                                    'http://wb.osf.io/file/test.csv?token=1234')
        renderer = TabularRenderer(metadata, test_csv_file_path, url, assets_url, export_url)
        body = renderer.render()
        assert BODY in body

    def test_render_tabular_csv_invalid(self, invalid_csv_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.csv', 'text/plain', '1234',
                                    'http://wb.osf.io/file/test.csv?token=1234')
        renderer = TabularRenderer(metadata, invalid_csv_file_path, url, assets_url, export_url)
        with pytest.raises(exceptions.EmptyTableError):
            renderer.render()


class TestTabularTsvRenderer:

    def test_render_tabular_tsv(self, test_tsv_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.tsv', 'text/plain', '1234',
                                    'http://wb.osf.io/file/test.tsv?token=1234')
        renderer = TabularRenderer(metadata, test_tsv_file_path, url, assets_url, export_url)
        body = renderer.render()
        assert BODY in body

    def test_render_tabular_tsv_invalid(self, invalid_tsv_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.tsv', 'text/plain', '1234',
                                    'http://wb.osf.io/file/test.tsv?token=1234')
        renderer = TabularRenderer(metadata, invalid_tsv_file_path, url, assets_url, export_url)
        with pytest.raises(exceptions.EmptyTableError):
            renderer.render()


class TestTabularXlsxRenderer:

    def test_render_tabular_xlsx(self, test_xlsx_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.xlsx', 'text/plain', '1234',
                                    'http://wb.osf.io/file/test.xlsx?token=1234')
        renderer = TabularRenderer(metadata, test_xlsx_file_path, url, assets_url, export_url)
        body = renderer.render()
        assert BODY in body

    def test_render_tabular_xlsx_invalid(self, invalid_xlsx_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.xlsx', 'text/plain', '1234',
                                    'http://wb.osf.io/file/test.xlsx?token=1234')
        renderer = TabularRenderer(metadata, invalid_xlsx_file_path, url, assets_url, export_url)
        with pytest.raises(XLRDError):
            renderer.render()


class TestTabularMatRenderer:

    def test_render_tabular_mat70(self, test_mat70_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.mat', 'text/plain', '1234',
                                    'http://wb.osf.io/file/testVer70.mat?token=1234')
        renderer = TabularRenderer(metadata, test_mat70_file_path, url, assets_url, export_url)
        body = renderer.render()
        assert BODY in body

    def test_render_tabular_mat70_invalid(self, invalid_mat70_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.mat', 'text/plain', '1234',
                                    'http://wb.osf.io/file/test.mat?token=1234')
        renderer = TabularRenderer(metadata, invalid_mat70_file_path, url, assets_url, export_url)
        with pytest.raises(exceptions.UnexpectedFormattingError):
            renderer.render()

    def test_render_tabular_mat73(self, test_mat73_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.mat', 'text/plain', '1234',
                                    'http://wb.osf.io/file/testVer74.mat?token=1234')
        renderer = TabularRenderer(metadata, test_mat73_file_path, url, assets_url, export_url)
        body = renderer.render()
        assert BODY in body

    def test_render_tabular_mat73_invalid(self, invalid_mat73_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.mat', 'text/plain', '1234',
                                    'http://wb.osf.io/file/test.mat?token=1234')
        renderer = TabularRenderer(metadata, invalid_mat73_file_path, url, assets_url, export_url)
        with pytest.raises(exceptions.UnexpectedFormattingError):
            renderer.render()
