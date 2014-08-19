import sys
import mfr
if not sys.version_info >= (3, 0):

    from mfr_docx import Handler as DocxFileHandler
    from mfr_docx.render import render_docx

    def setup_function(func):
        mfr.register_filehandler(DocxFileHandler)

    def test_detect_docx(fakefile):
        # set file's name
        fakefile.name = 'mydoc.docx'
        handler = DocxFileHandler()

        assert handler.detect(fakefile) is True

    def test_detect_nondocx(fakefile):
        fakefile.name = 'not_doc.odt'
        handler = DocxFileHandler()
        assert handler.detect(fakefile) is False

    def test_render_docx():
        with open('mfr_docx/fixtures/test.docx') as fp:
            result = render_docx(fp)

        assert type(result) == mfr.core.RenderResult
