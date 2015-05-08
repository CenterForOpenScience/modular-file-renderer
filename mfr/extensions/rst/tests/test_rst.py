import os

import pytest

import mfr
from mfr.ext import rst as mfr_rst

HERE = os.path.dirname(os.path.abspath(__file__))


def test_detect(fakefile):
    # set filename to have .rst extension
    fakefile.name = 'mydoc.rst'
    handler = mfr_rst.Handler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'other.rs',
    'otherrst',
    'other',
    'other.',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_rst.Handler()
    assert handler.detect(fakefile) is False


def test_render_rst_returns_render_result():
    with open(os.path.join(HERE, 'test.rst')) as fp:
        result = mfr_rst.render.render_rst(fp)

    assert type(result) == mfr.core.RenderResult
