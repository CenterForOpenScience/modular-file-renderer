import pytest

from mfr.core.provider import ProviderMetadata

from mfr.extensions.image import ImageRenderer
from mfr.extensions.image import settings


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.png', 'text/plain', '1234', 'http://wb.osf.io/file/test.png?token=1234')


@pytest.fixture
def file_path():
    return '/tmp/test.png'


@pytest.fixture
def url():
    return 'http://osf.io/file/test.png'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url={}&format={}.{}'.format(url(), settings.MAXIMUM_SIZE, settings.TYPE)


@pytest.fixture
def renderer(metadata, file_path, url, assets_url, export_url):
    return ImageRenderer(metadata, file_path, url, assets_url, export_url)


class TestImageRenderer:

    def test_render_image(self, renderer, export_url):
        body = renderer.render()
        assert '<img style="max-width: 100%;" src="{}">'.format(export_url) in body
