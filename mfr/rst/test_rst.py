
from mfr.rst.handler import RstFileHandler


def test_detect(fakefile):
    # set filename to have .rst extension
    fakefile.name = 'mydoc.rst'
    handler = RstFileHandler()
    assert handler.detect(fakefile) is True
