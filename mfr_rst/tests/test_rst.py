import pytest
import mfr
import mfr_rst


def test_detect(fakefile):
    # set filename to have .rst extension
    fakefile.name = 'mydoc.rst'
    handler = mfr_rst.Handler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'other.rs',
    'otherrst',
    'other',
    'other.',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_rst.Handler()
    assert handler.detect(fakefile) is False


def test_render_rst_returns_render_result():
    with open('mfr_rst/tests/test.rst') as fp:
        result = mfr_rst.render.render_rst(fp)

    assert type(result) == mfr.core.RenderResult
