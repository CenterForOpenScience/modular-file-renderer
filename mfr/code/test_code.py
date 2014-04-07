# -*- coding: utf-8 -*-
import pytest

from mfr.code.handler import CodeFileHandler


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
