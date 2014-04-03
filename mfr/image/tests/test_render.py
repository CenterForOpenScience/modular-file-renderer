# -*- coding: utf-8 -*-
"""Tests for the image renderer module."""
from mfr.image import ImageFileHandler

from mfr.image.render import render_img_tag


def test_render_img_tag(fakefile):
    result = render_img_tag(fakefile, src="/my/image.png", alt='My image')
    assert 'src="/my/image.png"' in result
    assert 'alt="My image"' in result


def test_image_handler_detect_image(fakefile):
    # set the file's name
    fakefile.name = 'myimage.jpg'

    handler = ImageFileHandler()
    assert handler.detect(fakefile) is True
