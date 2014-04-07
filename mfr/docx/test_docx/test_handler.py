from mfr.docx.handler import DocxFileHandler


def test_detect(fakefile):
    # set file's name
    fakefile.name = 'mydoc.docx'
    handler = DocxFileHandler()

    assert handler.detect(fakefile) is True
