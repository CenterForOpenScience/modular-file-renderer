# -*- coding: utf-8 -*-
"""Tests for the image renderer module."""

from mfr.image.render import render_img_tag
from mfr.image.handler import ImageFileHandler


def test_render_img_tag(fakefile):
    result = render_img_tag(fakefile, src="/my/image.png", alt='My image')
    assert 'src="/my/image.png"' in result
    assert 'alt="My image"' in result

# TODO: Move this to test_handler.py?
def test_image_handler_detect_image(fakefile):
    # set the file's name
    fakefile.name = 'myimage.jpg'

    handler = ImageFileHandler()
    assert handler.detect(fakefile) is True
