import pytest

from mfr.core.provider import ProviderMetadata
from mfr.extensions.video import VideoRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.mp4', 'text/plain', '1234',
                            'http://wb.osf.io/file/test.mp4?token=1234')


@pytest.fixture
def file_path():
    return '/tmp/test.mp4'


@pytest.fixture
def url():
    return 'http://osf.io/file/test.mp4'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, file_path, url, assets_url, export_url):
    return VideoRenderer(metadata, file_path, url, assets_url, export_url)


class TestVideoRenderer:

    def test_render_video(self, renderer, url):
        body = renderer.render()
        assert '<video controls' in body
        assert 'src="{}"'.format(metadata().download_url) in body
        assert '<style>body{margin:0;padding:0;}</style>' in ''.join(body.split())

    def test_render_video_file_required(self, renderer):
        assert renderer.file_required is False

    def test_render_video_cache_result(self, renderer):
        assert renderer.cache_result is False
