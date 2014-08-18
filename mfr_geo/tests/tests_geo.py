# -*- coding: utf-8 -*-
import pytest
import mfr
from mfr_geo import Handler as CodeFileHandler

def setup_function(func):
    mfr.register_filehandler(CodeFileHandler)
    mfr.config['STATIC_URL'] = '/static'


def teardown_function(func):
    mfr.core.reset_config()


@pytest.mark.parametrize('filename', [
    'script.geojson',
    'script.GeoJson',
    'script.Geojson',
    'script.GEOJSON',
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
    'other.json',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = CodeFileHandler()
    assert handler.detect(fakefile) is False
