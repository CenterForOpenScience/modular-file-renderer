from mfr.image.handler import ImageFileHandler, EXTENSIONS
from mfr.code.handler import EXTENSIONS as code_ext
import pytest
import mock
import mfr

mfr.register_filehandler('image', ImageFileHandler)

does_detect = ["test" + ext for ext in EXTENSIONS]
#todo (ajs) fill out list or find better way to do these
#todo (ajs) these will need to have actual image file data when we re-add imghdr detection
does_not_detect = ["test" + ext for ext in code_ext]


def make_mock(file_name, content=None):
    m = mock.Mock(spec=file)
    m.name = file_name
    m.read.return_value = content
    return m

## tests ##

# TODO: Move this to test_handler.py?
def test_image_handler_detect_image(fakefile):
    # set the file's name
    fakefile.name = 'myimage.jpg'

    handler = ImageFileHandler()
    assert handler.detect(fakefile) is True


def test_image_handler_does_detect():
    retvals = []
    for file_name in does_detect:
        rv = mfr.detect(make_mock(file_name))
        retvals.append(rv)
    assert False not in retvals


def test_image_handler_does_not_detect():
    retvals = []
    for file_name in does_not_detect:
        rv = mfr.detect(make_mock(file_name))
        retvals.append(rv)
    assert ImageFileHandler not in retvals
