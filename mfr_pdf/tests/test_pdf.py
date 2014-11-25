# -*- coding: utf-8 -*-
import pytest
import mfr
from mfr_pdf import Handler as CodeFileHandler
from mfr_pdf.render import is_valid

def setup_function(func):
    mfr.register_filehandler(CodeFileHandler)
    mfr.config['STATIC_URL'] = '/static'


def teardown_function(func):
    mfr.core.reset_config()


@pytest.mark.parametrize('filename', [
    'script.pdf',
    'script.PDF',
    'script.Pdf',
])
def test_detect_common_extensions(fakefile, filename):
    fakefile.name = filename
    handler = CodeFileHandler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'other.y',
    'otherpy',
    'other.bump',
    'other.',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = CodeFileHandler()
    assert handler.detect(fakefile) is False


def test_is_valid():
    result = is_valid('mfr_pdf/tests/test.pdf')
    assert result is True


#TODO(omdaniel) test that assets are included in the RenderResult
