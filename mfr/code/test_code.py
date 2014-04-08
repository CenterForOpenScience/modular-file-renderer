# -*- coding: utf-8 -*-
import pytest
import mfr
from mfr.code.handler import CodeFileHandler
from mfr.code.render import render_html
mfr.register_filehandler("code", CodeFileHandler)
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



