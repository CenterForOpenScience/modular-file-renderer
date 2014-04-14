import pytest
import mock
import mfr_libreoffice
from mfr_libreoffice.render import render

@pytest.mark.parametrize('filename', [
    'doc1.doc',
    'doc1.docx',
    'doc1.odt',
    'doc1.ott',
    'doc1.odp',
    'doc1.rtf',
    'doc1.ppt',
    'doc1.pptx',
    'doc1.xls',
    'doc1.xlsx',
    'doc1.csv',
    'doc1.ods', 
])

def test_detect_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_libreoffice.Handler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename',[
    'other.g',
    'otherjpg',
    'other.bump'
    'other.'
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_libreoffice.Handler()
    assert handler.detect(fakefile) is False

def test_render_failes(fakefile):
    fakefile.name = "doc1.doc"
    pytest.raises(ValueError, render, fakefile)

def test_render_html_files(fakefile):
    fakefile.name = "doc1.doc"
    with mock.patch("subprocess.call") as call_mock:
        call_mock.return_value = 0
        # the converted file is not actually created so it will raise an IOError
        pytest.raises(IOError, render, fakefile)

    with mock.patch("subprocess.call") as call_mock:
        result = render(fakefile)
        assert result.mimetype == 'text/html'
    
def test_render_pdf_files(fakefile):
    with mock.patch("subprocess.call") as call_mock:
        call_mock.return_value = 0
        fakefile.name = "doc1.ppt"

        try:
            render(fakefile)
        except IOError as e:
            # the result doesn't exist, still check that the expected output is a pdf
            assert e.filename.endswith(".pdf")
