import os
import shutil
from math import isclose

import pytest
from PIL import Image

from mfr.extensions.image import settings
from mfr.extensions.image import exceptions
from mfr.extensions.image import ImageExporter

BASE = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def directory(tmpdir):
    return str(tmpdir)


@pytest.fixture(scope="function", autouse=True)
def setup_filesystem(directory):
    shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)


class TestImageExporter:

    def test_jpg(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'test.jpg')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.jpg',
                            output_file_path=output_file_path, format=format)

        assert not os.path.exists(output_file_path)
        assert os.path.exists(directory)

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
            assert isclose(source_pixels[i][0], output_pixels[i][0], abs_tol=1)
            assert isclose(source_pixels[i][1], output_pixels[i][1], abs_tol=1)
            assert isclose(source_pixels[i][2], output_pixels[i][2], abs_tol=1)

    def test_jpeg(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'test.jpeg')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.jpeg',
                            output_file_path=output_file_path, format=format)

        assert not os.path.exists(output_file_path)
        assert os.path.exists(directory)

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
            assert isclose(source_pixels[i][0], output_pixels[i][0], abs_tol=5)
            assert isclose(source_pixels[i][1], output_pixels[i][1], abs_tol=5)
            assert isclose(source_pixels[i][2], output_pixels[i][2], abs_tol=5)

    def test_psd(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'test.psd')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.psd',
                            output_file_path=output_file_path, format=format)

        assert not os.path.exists(output_file_path)
        assert os.path.exists(directory)

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
            assert isclose(source_pixels[i][0], output_pixels[i][0], abs_tol=5)
            assert isclose(source_pixels[i][1], output_pixels[i][1], abs_tol=5)
            assert isclose(source_pixels[i][2], output_pixels[i][2], abs_tol=5)

    def test_png(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'test.png')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.png',
                            output_file_path=output_file_path, format=format)

        assert not os.path.exists(output_file_path)
        assert os.path.exists(directory)

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
            # This conversion changes some pixels wildy... So high tolerance
            assert isclose(source_pixels[i][0], output_pixels[i][0], abs_tol=20)
            assert isclose(source_pixels[i][1], output_pixels[i][1], abs_tol=20)
            assert isclose(source_pixels[i][2], output_pixels[i][2], abs_tol=20)

    def test_png_with_transparency(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'test_transparency.png')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.png',
                            output_file_path=output_file_path, format=format)

        assert not os.path.exists(output_file_path)
        assert os.path.exists(directory)

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
            # Being zero means it was most likely transparent, and got converted to white.
            assert isclose(source_pixels[i][0], output_pixels[i][0], abs_tol=5) or (
                isclose(0, source_pixels[i][0], abs_tol=1))
            assert isclose(source_pixels[i][1], output_pixels[i][1], abs_tol=5) or (
                isclose(0, source_pixels[i][1], abs_tol=1))
            assert isclose(source_pixels[i][2], output_pixels[i][2], abs_tol=5) or (
                isclose(0, source_pixels[i][2], abs_tol=1))

    def test_bmp(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'test.bmp')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.bmp',
                            output_file_path=output_file_path, format=format)

        assert not os.path.exists(output_file_path)
        assert os.path.exists(directory)

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
        source_file_path = os.path.join(BASE, 'files', 'test_ratio.png')
        output_file_path = os.path.join(directory, 'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.png',
                            output_file_path=output_file_path, format=format)

        assert not os.path.exists(output_file_path)
        assert os.path.exists(directory)

        exporter.export()

        assert os.path.exists(output_file_path)

        output_image = Image.open(output_file_path)
        source_image = Image.open(source_file_path)

        assert output_image.mode == 'RGB'
        assert output_image.size == (1200, 1029)
        assert output_image.palette == source_image.palette
        assert output_image.format.lower() == settings.EXPORT_TYPE

    def test_exceptions(self, directory):
        source_file_path = os.path.join(BASE, 'files', 'test.jpg')
        output_file_path = os.path.join(directory, 'fake', 'place',
                            'test.{}'.format(settings.EXPORT_TYPE))
        format = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)
        exporter = ImageExporter(source_file_path=source_file_path, ext='.jpg',
                            output_file_path=output_file_path, format=format)

        assert not os.path.exists(output_file_path)
        assert os.path.exists(directory)
        with pytest.raises(exceptions.PillowImageError) as e:
            exporter.export()
        assert e.value.code == 400
