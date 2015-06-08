import os
import pytest

from mfr.extensions.tabular import settings
from mfr.extensions.tabular import TabularRenderer
from pandas.parser import CParserError
from xlrd.biffh import XLRDError


@pytest.fixture
def url():
    return 'http://osf.io/file/test.csv'


@pytest.fixture
def download_url():
    return 'http://wb.osf.io/file/test.csv?token=1234'


@pytest.fixture
def test_csv_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.csv')


@pytest.fixture
def invalid_csv_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.csv')


@pytest.fixture
def test_tsv_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.tsv')


@pytest.fixture
def invalid_tsv_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.tsv')


@pytest.fixture
def test_xlsx_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.xlsx')


@pytest.fixture
def invalid_xlsx_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.xlsx')


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def renderer(url, download_url, test_csv_file_path, assets_url, extension='.csv'):
    return TabularRenderer(url, download_url, test_csv_file_path, assets_url, extension)


class TestTabularRenderer:

    def test_render_tabular_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_tabular_cache_result(self, renderer):
        assert renderer.cache_result is True


class TestTabularCsvRenderer:

    def test_render_tabular_csv(self, url, download_url, test_csv_file_path, assets_url, extension='.csv'):
        renderer = TabularRenderer(url, download_url, test_csv_file_path, assets_url, extension)
        body = renderer.render()
        assert '<div id="mfrViewer" style="min-height: {}px;"></div>'.format(settings.TABLE_HEIGHT) in body

    def test_render_tabular_csv_invalid(self, url, download_url, invalid_csv_file_path, assets_url, extension='.csv'):
        renderer = TabularRenderer(url, download_url, invalid_csv_file_path, assets_url, extension)
        with pytest.raises(CParserError):
            renderer.render()


class TestTabularTsvRenderer:

    def test_render_tabular_tsv(self, url, download_url, test_tsv_file_path, assets_url, extension='.tsv'):
        renderer = TabularRenderer(url, download_url, test_tsv_file_path, assets_url, extension)
        body = renderer.render()
        assert '<div id="mfrViewer" style="min-height: {}px;"></div>'.format(settings.TABLE_HEIGHT) in body

    def test_render_tabular_tsv_invalid(self, url, download_url, invalid_tsv_file_path, assets_url, extension='.tsv'):
        renderer = TabularRenderer(url, download_url, invalid_tsv_file_path, assets_url, extension)
        with pytest.raises(ValueError):
            renderer.render()


class TestTabularXlsxRenderer:

    def test_render_tabular_xlsx(self, url, download_url, test_xlsx_file_path, assets_url, extension='.xlsx'):
        renderer = TabularRenderer(url, download_url, test_xlsx_file_path, assets_url, extension)
        body = renderer.render()
        assert '<div id="mfrViewer" style="min-height: {}px;"></div>'.format(settings.TABLE_HEIGHT) in body

    def test_render_tabular_xlsx_invalid(self, url, download_url, invalid_xlsx_file_path, assets_url, extension='.xlsx'):
        renderer = TabularRenderer(url, download_url, invalid_xlsx_file_path, assets_url, extension)
        with pytest.raises(XLRDError):
            renderer.render()
