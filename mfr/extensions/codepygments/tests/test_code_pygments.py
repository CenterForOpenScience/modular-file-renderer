# -*- coding: utf-8 -*-
import os
import pytest

import mfr
from mfr.ext.code_pygments import Handler as CodeFileHandler
from mfr.ext.code_pygments.render import get_stylesheet, render_html
from mfr.ext.code_pygments.configuration import config

HERE = os.path.dirname(os.path.abspath(__file__))


def setup_function(func):
    mfr.register_filehandler(CodeFileHandler)
    mfr.config['ASSETS_URL'] = '/static'


def teardown_function(func):
    mfr.core.reset_config()


@pytest.mark.parametrize('filename', [
    'script.py',
    'script.rb',
    'script.js',
    'script.PY',
    'script.RB',
    'script.JS',
    'script.md',
    'script',
])
def test_detect_common_extensions(fakefile, filename):
    fakefile.name = filename
    handler = CodeFileHandler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'other.y',
    'other.bump',
    'other.',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = CodeFileHandler()
    assert handler.detect(fakefile) is False


def test_get_stylesheet():
    result = get_stylesheet()
    expected_url = '{0}/code_pygments/css/default.css'.format(
        mfr.config['ASSETS_URL'])
    assert expected_url == result


def test_configuration_defaults():
    assert config['PYGMENTS_THEME'] == 'default'
    assert config['CSS_CLASS'] == 'codehilite'


def test_render_returns_render_result():
    with open(os.path.join(HERE, 'test_code_pygments.py')) as fp:
        result = render_html(fp)

    assert type(result) == mfr.core.RenderResult

def test_renders_md():
    with open(os.path.join(HERE, 'foo.md')) as fp:
        result = render_html(fp)

    assert type(result) == mfr.core.RenderResult
