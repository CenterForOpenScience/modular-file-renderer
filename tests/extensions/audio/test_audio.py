import pytest

from mfr.extensions.audio import AudioRenderer


@pytest.fixture
def url():
    return 'test.mp3'


@pytest.fixture
def file_path():
    return {}


@pytest.fixture
def assets_url():
    return {}


@pytest.fixture
def extension():
    return {}


@pytest.fixture
def renderer(url, file_path, assets_url, extension):
    return AudioRenderer(url, file_path, assets_url, extension)


class TestAudio:

    @pytest.mark.parametrize('filename', [
        'sheet.csv',
        'sheet.tsv',
        'sheet.CSV',
        'sheet.TSV',
        'sheet.xlsx',
        'sheet.XLSX',
        'sheet.xls',
        'sheet.XLS',
        'sheet.dta',
        'sheet.DTA',
        'sheet.sav',
        'sheet.SAV',
        # 'sheet.ods',
        # 'sheet.ODS',
    ])
    def test_render_audio(self, renderer, filename):
        html = renderer.render()
