from math import isclose
import os
import shutil

from PIL import Image
import pytest

from mfr.extensions.image import exceptions, ImageExporter, settings


BASE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def directory(tmpdir):
    return str(tmpdir)


@pytest.fixture(scope="function", autouse=True)
def setup_filesystem(directory):
    shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)


class TestImageExporter:

    @pytest.mark.parametrize("file_name,tolerance", [
        ('test.jpg', 1),
        ('test.jpeg', 5),
        ('test.psd', 5),
        ('test.png', 20),
    ])
    def test_jpg(self, directory, file_name, tolerance):
        source_file_path = os.path.join(BASE, 'files', file_name)
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.jpg',
                                 output_file_path=output_file_path, format=format,
                                 metadata={})

        assert not os.path.exists(output_file_path)

        exporter.export()

        assert os.path.exists(output_file_path)

        output_image = Image.open(output_file_path)
        source_image = Image.open(source_file_path)
        source_pixels = list(source_image.getdata())
        output_pixels = list(output_image.getdata())

        assert source_image.size == output_image.size
        assert output_image.mode == 'RGB'
        assert output_image.palette == source_image.palette
        assert output_image.format.lower() == settings.EXPORT_TYPE

        for i in range(100):
            # PIL conversions change some pixels, but first 100 are the same on this one
            assert isclose(source_pixels[i][0], output_pixels[i][0], abs_tol=tolerance)
            assert isclose(source_pixels[i][1], output_pixels[i][1], abs_tol=tolerance)
            assert isclose(source_pixels[i][2], output_pixels[i][2], abs_tol=tolerance)

    def test_png_with_transparency(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'test_transparency.png')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.png',
                                 output_file_path=output_file_path, format=format,
                                 metadata={})

        assert not os.path.exists(output_file_path)

        exporter.export()

        assert os.path.exists(output_file_path)

        output_image = Image.open(output_file_path)
        source_image = Image.open(source_file_path)
        source_pixels = list(source_image.getdata())
        output_pixels = list(output_image.getdata())

        assert source_image.size == output_image.size
        assert output_image.mode == 'RGB'
        assert output_image.palette == source_image.palette
        assert output_image.format.lower() == settings.EXPORT_TYPE
        for i in range(100):
            # Check if conversion is close OR if the value on the source is 0. A value on the source
            # being zero means it was most likely transparent, and got converted to white.
            assert (
                isclose(source_pixels[i][0], output_pixels[i][0], abs_tol=5) and
                isclose(source_pixels[i][1], output_pixels[i][1], abs_tol=5) and
                isclose(source_pixels[i][2], output_pixels[i][2], abs_tol=5)
            ) or (
                isclose(0, source_pixels[i][0], abs_tol=1) and
                isclose(0, source_pixels[i][1], abs_tol=1) and
                isclose(0, source_pixels[i][2], abs_tol=1))

    def test_bmp(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'test.bmp')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.bmp',
                                 output_file_path=output_file_path, format=format,
                                 metadata={})

        assert not os.path.exists(output_file_path)

        exporter.export()

        assert os.path.exists(output_file_path)

        output_image = Image.open(output_file_path)
        source_image = Image.open(source_file_path)
        output_pixels = list(output_image.getdata())

        assert source_image.size == output_image.size
        assert output_image.mode == 'RGB'
        assert output_image.palette == source_image.palette
        assert output_image.format.lower() == settings.EXPORT_TYPE
        # looped pixel tests not included because values varried so much that
        # they were basically useless
        assert output_pixels[0] == (255, 254, 232)

    def test_ratio(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'test_ratio.jpg')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.png',
                                 output_file_path=output_file_path, format=format,
                                 metadata={})

        assert not os.path.exists(output_file_path)

        exporter.export()

        assert os.path.exists(output_file_path)

        output_image = Image.open(output_file_path)
        source_image = Image.open(source_file_path)

        assert output_image.mode == 'RGB'
        assert output_image.size == (2400, 1600)
        assert output_image.palette == source_image.palette
        assert output_image.format.lower() == settings.EXPORT_TYPE

    def test_exception_file_not_found(self, directory):
        # triggers a `FileNotFoundError`
        source_file_path = os.path.join(BASE, 'files', 'test.jpg')
        output_file_path = os.path.join(directory, 'fake', 'place',
                                        'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.jpg',
                                 output_file_path=output_file_path, format=format,
                                 metadata={})

        assert not os.path.exists(output_file_path)
        with pytest.raises(exceptions.PillowImageError) as e:
            exporter.export()
        assert e.value.code == 400

    def test_exception_courrupt_file(self, directory):
        # triggers an OSError with a corrupt file
        source_file_path = os.path.join(BASE, 'files', 'invalid.jpg')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.jpg',
                                 output_file_path=output_file_path, format=format,
                                 metadata={})

        assert not os.path.exists(output_file_path)
        with pytest.raises(exceptions.PillowImageError) as e:
            exporter.export()
        assert e.value.code == 400
