# -*- coding: utf-8 -*-
import os

import pytest
import mfr
import sys
import urllib

pytestmark = pytest.mark.skipif(sys.version_info > (3, 0), reason="Python 3.x doesn't support end-relative seeks\
                                which PyPDF2 uses when rendering")  # noqa

from mfr.ext.pdf import Handler as PdfHandler
from mfr.ext.pdf.render import is_valid, render_pdf

HERE = os.path.dirname(os.path.abspath(__file__))


def setup_function(func):
    mfr.register_filehandler(PdfHandler)


def teardown_function(func):
    mfr.core.reset_config()


@pytest.mark.parametrize('filename', [
    'script.pdf',
    'script.PDF',
    'script.Pdf',
])
def test_detect_common_extensions(fakefile, filename):
    fakefile.name = filename
    handler = PdfHandler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'other.y',
    'otherpy',
    'other.bump',
    'other.',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = PdfHandler()
    assert handler.detect(fakefile) is False


def test_is_valid():
    result = is_valid(os.path.join(HERE, 'test.pdf'))
    assert result is True


def test_is_not_valid():
    result = is_valid(os.path.join(HERE, 'invalid.pdf'))
    assert result is False


def test_render_pdf():
    mfr.config['ASSETS_URL'] = "fake/url"
    with open(os.path.join(HERE, 'test.pdf')) as fp:
        result = render_pdf(fp)
    assert result.content is not None


def test_render_invalid_pdf():
    mfr.config['ASSETS_URL'] = "fake/url"
    with open(os.path.join(HERE, 'invalid.pdf')) as fp:
        result = render_pdf(fp)
    assert result.content == "This is not a valid pdf file"


def test_src_in_rendered_content():
    mfr.config['ASSETS_URL'] = "fake/url"
    with open(os.path.join(HERE, 'test.pdf')) as fp:
        result = render_pdf(fp)
    url_encoded_src = urllib.quote_plus(fp.name)
    assert url_encoded_src in result.content
