# -*- coding: utf-8 -*-
import pytest
import mfr
from mfr_pdf import Handler as PdfFileHandler


def setup_function(func):
    mfr.register_filehandler(PdfFileHandler)
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
    handler = PdfFileHandler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'other.y',
    'otherpy',
    'other.bump',
    'other.',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = PdfFileHandler()
    assert handler.detect(fakefile) is False
