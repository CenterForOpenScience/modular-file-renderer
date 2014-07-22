# -*- coding: utf-8 -*-
import pytest
import mfr
from mfr_code_pygments import Handler as CodeFileHandler
from mfr_code_pygments.render import get_stylesheet

from mfr_code_pygments.configuration import config


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
    expected_url = '{0}/mfr_code_pygments/css/default.css'.format(mfr.config['STATIC_URL'])
    assert expected_url in result


#TODO(asmacdo) test that assets are included in the RenderResult

def test_configuration_defaults():
    assert config['PYGMENTS_THEME'] == 'default'
    assert config['CSS_CLASS'] == 'codehilite'
