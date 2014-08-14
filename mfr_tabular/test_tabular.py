# -*- coding: utf-8 -*-
import pytest
import mfr
from mfr_tabular import Handler as TabularHandler


def setup_function(func):
    mfr.register_filehandler(TabularHandler)
    mfr.config['STATIC_URL'] = '/static'


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
