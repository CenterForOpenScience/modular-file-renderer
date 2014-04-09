# -*- coding: utf-8 -*-
import pytest
import mfr
from mfr.code.handler import CodeFileHandler
from mfr.code.render import render_html, get_stylesheet

def setup_function(func):
    mfr.register_filehandler("code", CodeFileHandler)
    mfr.config['STATIC_URL'] = '/static'

@pytest.mark.parametrize('filename', [
    'script.py',
    'script.rb',
    'script.js',
    'script.PY',
    'script.RB',
    'script.JS',
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


def test_get_stylesheet():
    result = get_stylesheet()
    expected_url = '{0}/code/css/style.css'.format(mfr.config['STATIC_URL'])
    assert expected_url in result
