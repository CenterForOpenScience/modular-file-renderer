import os
import sys

import pytest

import mfr

HERE = os.path.dirname(os.path.abspath(__file__))

# Pydocx .3.14 does not support python 3
if not sys.version_info >= (3, 0):

    from mfr.ext.docx import Handler as DocxFileHandler
    from mfr.ext.docx.render import render_docx


@pytest.mark.skipif(sys.version_info >= (3, 0),
                    reason="pydocx 0.3.14 does not support py3")
def setup_function(func):
    mfr.register_filehandler(DocxFileHandler)


@pytest.mark.skipif(sys.version_info >= (3, 0),
                    reason="pydocx 0.3.14 does not support py3")
def test_detect_docx(fakefile):
    # set file's name
    fakefile.name = 'mydoc.docx'
    handler = DocxFileHandler()

    assert handler.detect(fakefile) is True


@pytest.mark.skipif(sys.version_info >= (3, 0),
                    reason="pydocx 0.3.14 does not support py3")
def test_detect_nondocx(fakefile):
    fakefile.name = 'not_doc.odt'
    handler = DocxFileHandler()
    assert handler.detect(fakefile) is False


@pytest.mark.skipif(sys.version_info >= (3, 0),
                    reason="pydocx 0.3.14 does not support py3")
def test_render_docx():
    with open(os.path.join(HERE, 'test.docx')) as fp:
        result = render_docx(fp)

    assert type(result) == mfr.core.RenderResult
