import pytest
import sys
from mfr.ext import image as mfr_image
from ..render import render_img_tag

@pytest.mark.parametrize('filename', [
    'image.jpeg',
    'image.png',
    'image.jpg',
    'image.bmp',
    'image.JPEG',
    'image.PNG',
    'image.JPG',
    'image.BMP',
    'image.Jpeg',
    'image.pnG',
])
def test_detect_image_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_image.Handler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'other.g',
    'otherjpg',
    'other.bump',
    'other.',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_image.Handler()
    assert handler.detect(fakefile) is False


def test_render_img_tag(fakefile):
    result = render_img_tag(fakefile, src="/my/image.png", alt='My image')
    assert 'src="/my/image.png"' in result
    assert 'alt="My image"' in result


@pytest.mark.skipif(sys.version_info[0] > 2, reason="requires python2.7 or less")
def test_export_jpg():
    handler = mfr_image.Handler()
    exporter = mfr_image.ImageExporter()
    with open('mfr/ext/image/tests/test_jpg.jpg') as fp:
        jpeg_img = exporter.export_jpeg(fp)
        fp.seek(0)
        png_img = exporter.export_png(fp)
        fp.seek(0)
        tif_img = exporter.export_tif(fp)
        fp.seek(0)
        gif_img = exporter.export_gif(fp)
    if type(jpeg_img) != str:
        assert handler.detect(jpeg_img) is True
        assert handler.detect(png_img) is True
        assert handler.detect(tif_img) is True
        assert handler.detect(gif_img) is True
    else:
        assert "Unable to export" in jpeg_img
        assert "Unable to export" in png_img
        assert "Unable to export" in tif_img
        assert "Unable to export" in gif_img
