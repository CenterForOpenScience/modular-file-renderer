# # -*- coding: utf-8 -*-
# import os
#
# import pytest
# import mfr
# import urllib
#
# from mfr.ext.pdf import Handler as PdfHandler
# from mfr.ext.pdf.render import render_html
#
# HERE = os.path.dirname(os.path.abspath(__file__))
#
#
# def setup_function(func):
#     mfr.register_filehandler(PdfHandler)
#
#
# def teardown_function(func):
#     mfr.core.reset_config()
#
#
# @pytest.mark.parametrize('filename', [
#     'script.pdf',
#     'script.PDF',
#     'script.Pdf',
# ])
# def test_detect_common_extensions(fakefile, filename):
#     fakefile.name = filename
#     handler = PdfHandler()
#     assert handler.detect(fakefile) is True
#
#
# @pytest.mark.parametrize('filename', [
#     'other.y',
#     'otherpy',
#     'other.bump',
#     'other.',
# ])
# def test_does_not_detect_other_extensions(fakefile, filename):
#     fakefile.name = filename
#     handler = PdfHandler()
#     assert handler.detect(fakefile) is False
#
#
# def test_render_pdf():
#     mfr.config['ASSETS_URL'] = 'fake/url'
#     src = 'http://www.cos.io/test.pdf'
#     encoded_src = src.replace("'", "\\'")
#     with open(os.path.join(HERE, 'test.pdf')) as fp:
#         result = render_html(fp, src)
#     assert result.content is not None
#     assert encoded_src in result.content
