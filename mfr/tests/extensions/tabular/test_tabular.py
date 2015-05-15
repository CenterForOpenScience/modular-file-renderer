# -*- coding: utf-8 -*-
import os
import pytest
import mfr
from mfr.extensions.tabular.render import render_html
from mfr.extensions.tabular import Handler as TabularHandler

HERE = os.path.dirname(os.path.abspath(__file__))

def setup_function(func):
    mfr.register_filehandler(TabularHandler)
    mfr.config['ASSETS_URL'] = '/static'


def teardown_function(func):
    mfr.core.reset_config()


# Some ods files work, but it is very inconsistent. Turning off for now.
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
def test_detect_extensions(fakefile, filename):
    fakefile.name = filename
    handler = TabularHandler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'sheet.py',
    'sheet.invalid',
    'sheet',
    '',
    'sheet.',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = TabularHandler()
    assert handler.detect(fakefile) is False


def test_render_html_returns_render_result():
    with open(os.path.join(HERE, 'fixtures', 'test.csv')) as fp:
        result = render_html(fp)

    assert type(result) == mfr.RenderResult
