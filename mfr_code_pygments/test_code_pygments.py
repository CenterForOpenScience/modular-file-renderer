# -*- coding: utf-8 -*-
import pytest
import mfr
from mfr_code_pygments import Handler as CodeFileHandler
from mfr_code_pygments.render import get_stylesheet


def setup_function(func):
    mfr.register_filehandler(CodeFileHandler)
    mfr.config['STATIC_URL'] = '/static'


def teardown_function(func):
    mfr.core.reset_config()


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

def test_stylesheet_not_included_by_default(fakefile):
    fakefile.name = 'zen.py'
    fakefile.read.return_value = 'import this'
    rendered = CodeFileHandler().render(fakefile)
    assert get_stylesheet() not in rendered

def test_stylesheet_included_if_include_static_is_true(fakefile):
    mfr.config['INCLUDE_STATIC'] = True
    fakefile.name = 'zen.py'
    fakefile.read.return_value = 'import this'
    rendered = CodeFileHandler().render(fakefile)
    assert get_stylesheet() in rendered
