import pytest
from mfr.image.render import render_img_tag
from mfr.image.handler import ImageFileHandler

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
    handler = ImageFileHandler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename',[
    'other.g',
    'otherjpg',
    'other.bump'
    'other.'
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = ImageFileHandler()
    assert handler.detect(fakefile) is False


def test_render_img_tag(fakefile):
    result = render_img_tag(fakefile, src="/my/image.png", alt='My image')
    assert 'src="/my/image.png"' in result
    assert 'alt="My image"' in result
