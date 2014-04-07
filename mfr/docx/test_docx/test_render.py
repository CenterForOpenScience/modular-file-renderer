# -*- coding: utf-8 -*-

from mfr.docx.render import render_TEMPLATE_tag


def test_render_TEMPLATE_tag(fakefile):
    ### Testing stuff###
    result = render_TEMPLATE_tag(fakefile, src="/my/file.SAMPLE", alt='My SAMPLE')
    assert 'src="/my/file.SAMPLE"' in result
    assert 'alt="My SAMPLE"' in result

