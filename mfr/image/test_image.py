import pytest
from mfr.image.render import render_img_tag
from mfr.image.handler import ImageFileHandler

@pytest.mark.parametrize('filename', [
    'image.jpeg',
    'image.png',
    'image.jpg',
    'image.bmp',
])


def test_detect_image_extensions(fakefile, filename):
    fakefile.name = filename
    handler = ImageFileHandler()
    assert handler.detect(fakefile) is True


def test_render_img_tag(fakefile):
    result = render_img_tag(fakefile, src="/my/image.png", alt='My image')
    assert 'src="/my/image.png"' in result
    assert 'alt="My image"' in result
