import os

import pytest

import mfr
from mfr.ext import pdb as mfr_pdb

HERE = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize('filename', [
    'protein.pdb',
    'protein.PDB',
    'protein.pDb',
])
def test_detect_protein_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_pdb.Handler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'otherpdb',
    'other.protein',
    'other',
    'other.p',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_pdb.Handler()
    assert handler.detect(fakefile) is False


def test_render_html_returns_render_result():
    mfr.config['ASSETS_URL'] = "fake/url"
    src = 'http://www.cos.io/test.pdb'
    encoded_src = src.replace("'", "\\'")
    with open(os.path.join(HERE, 'test.pdb')) as fp:
        result = mfr_pdb.render_html(fp,src)

    assert type(result) == mfr.core.RenderResult
    assert encoded_src in result.content
