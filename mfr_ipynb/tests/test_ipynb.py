import mock
import mfr
from mfr import RenderResult
import pytest
from mfr_ipynb import Handler as CodeFileHandler
from mfr_ipynb.render import render_html
import sys

@pytest.mark.skipif(sys.version_info < (2,7),
                    reason="requires python2.7+")

def test_detect_correct_extension(fakefile):
    fakefile.name = 'hello.ipynb'
    handler = CodeFileHandler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'other.y',
    'otherpy',
    'other.bump',
    'other.',
])
def test_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = CodeFileHandler()
    assert handler.detect(fakefile) is False
# flake8: noqa