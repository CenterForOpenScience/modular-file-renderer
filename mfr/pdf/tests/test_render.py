# -*- coding: utf-8 -*-
"""Tests for the TEMPLATE renderer module."""

from mfr.TEMPLATE.render import render_TEMPLATE_tag
from mfr.TEMPLATE.handler import TEMPLATEFileHandler


def test_render_TEMPLATE_tag(fakefile):
    ### Testing stuff###
    result = render_TEMPLATE_tag(fakefile, src="/my/file.SAMPLE", alt='My SAMPLE')
    assert 'src="/my/file.SAMPLE"' in result
    assert 'alt="My SAMPLE"' in result



# TODO: Move this to test_handler.py?
def test_TEMPLATE_handler_detect_TEMPLATE(fakefile):
    # set the file's name
    fakefile.name = 'file.SAMPLE'

    handler = TEMPLATEFileHandler()
    assert handler.detect(fakefile) is True
