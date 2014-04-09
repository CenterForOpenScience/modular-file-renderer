
import mfr_rst


def test_detect(fakefile):
    # set filename to have .rst extension
    fakefile.name = 'mydoc.rst'
    handler = mfr_rst.Handler()
    assert handler.detect(fakefile) is True
