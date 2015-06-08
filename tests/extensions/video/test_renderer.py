import pytest

from mfr.extensions.video import VideoRenderer


@pytest.fixture
def url():
    return 'http://osf.io/file/test.mp4'


@pytest.fixture
def download_url():
    return 'http://wb.osf.io/file/test.mp4?token=1234'


@pytest.fixture
def file_path():
    return '/tmp/test.mp4'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def extension():
    return '.mp3'


@pytest.fixture
def renderer(url, download_url, file_path, assets_url, extension):
    return VideoRenderer(url, download_url, file_path, assets_url, extension)


class TestVideoRenderer:

    def test_render_video(self, renderer, url):
        body = renderer.render()
        assert '<video controls' in body
        assert 'src="{}"'.format(url) in body

    def test_render_video_file_required(self, renderer):
        assert renderer.file_required is False

    def test_render_video_cache_result(self, renderer):
        assert renderer.cache_result is False
