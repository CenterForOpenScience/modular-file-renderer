# -*- coding: utf-8 -*-
import pytest
import mfr
import sys

pytestmark = pytest.mark.skipif(sys.version_info > (3, 0), reason="Python 3.x doesn't support end-relative seeks\
                                which PyPDF2 uses when rendering")  # noqa

from mfr_pdf import Handler as CodeFileHandler
from mfr_pdf.render import is_valid, get_assets, render_pdf

def setup_function(func):
    mfr.register_filehandler(CodeFileHandler)
    mfr.config['ASSETS_URL'] = '/static'


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

def test_is_not_valid():
    result = is_valid('mfr_pdf/tests/invalid.pdf')
    assert result is False

def test_get_assets():
    assets = get_assets()
    assert type(assets) is dict
    assert assets is not None

def test_render_pdf():
    with open('mfr_pdf/tests/test.pdf') as fp:
        result = render_pdf(fp)
    assert result.content is not None
    assert result.assets is not None

def test_render_invalid_pdf():
    with open('mfr_pdf/tests/invalid.pdf') as fp:
        result = render_pdf(fp)
    assert result.content == "This is not a valid pdf file"
