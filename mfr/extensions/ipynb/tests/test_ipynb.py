import os
import sys

import pytest

pytestmark = pytest.mark.skipif(sys.version_info < (2, 7), reason="requires python2.7+")  # noqa

import mfr
from mfr.ext.ipynb import Handler as CodeFileHandler

HERE = os.path.dirname(os.path.abspath(__file__))

def setup_function(func):
    mfr.register_filehandler(CodeFileHandler)
    mfr.config['ASSETS_URL'] = '/static'


def teardown_function(func):
    mfr.core.reset_config()


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


def test_render_html():
    from ..render import render_html
    handler = CodeFileHandler()
    mfr.register_filehandler(handler)
    with open(os.path.join(HERE, 'test.ipynb')) as fp:
        result = render_html(fp)
    assert result.content is not None
    assert "pygments" in str(result.assets['css'])


def test_invalid_file():
    from ..render import render_html
    handler = CodeFileHandler()
    mfr.register_filehandler(handler)
    with open(os.path.join(HERE, 'invalid_json.ipynb')) as fp:
        result = render_html(fp)
    assert 'Invalid json: ' in result.content


def test_get_metadata():
    from ..render import get_metadata
    with open(os.path.join(HERE, 'test.ipynb')) as fp:
        name, css = get_metadata(fp)
    assert name == 'zipline pydata12'
    assert css == 'something.css'


def test_no_metadata():
    from ..render import get_metadata
    with open(os.path.join(HERE, 'no_metadata.ipynb')) as fp:
        name, css = get_metadata(fp)
    assert name == 'untitled'
    assert css is None


def test_invalid_json_metadata():
    from ..render import get_metadata
    with open(os.path.join(HERE, 'invalid_json.ipynb')) as fp:
        name, css = get_metadata(fp)
    assert name == 'Unable to parse json'
    assert css == 'No metadata found'
