import pytest

from mfr.extensions.image import ImageRenderer


@pytest.fixture
def url():
    return 'http://osf.io/file/test.png'


@pytest.fixture
def download_url():
    return 'http://wb.osf.io/file/test.png?token=1234'


@pytest.fixture
def file_path():
    return '/tmp/test.png'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def extension():
    return '.png'


@pytest.fixture
def renderer(url, download_url, file_path, assets_url, extension):
    return ImageRenderer(url, download_url, file_path, assets_url, extension)


class TestImageRenderer:

    def test_render_image(self, renderer, url):
        body = renderer.render()
        assert '<img style="max-width: 100%;" src="{}">'.format(url) in body
