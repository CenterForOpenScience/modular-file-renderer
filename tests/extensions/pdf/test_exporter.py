import os
import shutil
import binascii

import pytest

from mfr.extensions.pdf import (settings,
                                exceptions,
                                PdfExporter)


BASE = os.path.dirname(os.path.abspath(__file__))

# Should be the first 4 bytes of a pdf file
PDF_SIG = b'25504446'


@pytest.fixture
def directory(tmpdir):
    return str(tmpdir)


@pytest.fixture(scope="function", autouse=True)
def setup_filesystem(directory):
    shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)


class TestPdfExporter:
    '''
    The PdfExporter uses the `report-lab` library to turn tiffs into pdfs.
    However, opening and verifying pdfs for testing purposes is a paid feature of
    `report-lab`. Instead we will manually open them and just check the signature.
    '''

    @pytest.mark.parametrize("file_name", [
        ('test.tif'),
        ('test_multipage.tif'),
        ('test_ratio.tif'),
        # On old Pillow versions this would fail to open. Should open fin on 4.3.0
        ('test_broken.tif'),
    ])
    def test_single_page_tiff(self, directory, file_name):
        source_file_path = os.path.join(BASE, 'files', file_name)
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = PdfExporter(source_file_path=source_file_path, ext='.tif',
                               output_file_path=output_file_path, format=format,
                               metadata={'unique_key': 'moo moo moo'})

        assert not os.path.exists(output_file_path)

        exporter.export()

        assert os.path.exists(output_file_path)
        # Open file to check that the exported PDF contains the proper signature
        with open(output_file_path, 'rb') as file:
            # the first 4 bytes contain the signature
            assert binascii.hexlify(file.read(4)) == PDF_SIG

    def test_bad_tiff(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'invalid.tif')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = PdfExporter(source_file_path=source_file_path, ext='.tif',
                               output_file_path=output_file_path, format=format,
                               metadata={'unique_key': 'moo moo moo'})

        assert not os.path.exists(output_file_path)

        with pytest.raises(exceptions.PillowImageError):
            exporter.export()
