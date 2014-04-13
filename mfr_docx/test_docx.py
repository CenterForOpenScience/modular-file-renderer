from mfr_docx import Handler as DocxFileHandler


def test_detect_docx(fakefile):
    # set file's name
    fakefile.name = 'mydoc.docx'
    handler = DocxFileHandler()

    assert handler.detect(fakefile) is True

def test_detect_nondocx(fakefile):
    fakefile.name = 'not_doc.odt'
    handler = DocxFileHandler()
    assert handler.detect(fakefile) is False
