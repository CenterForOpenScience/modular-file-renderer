import pytest

from mfr.extensions.audio import AudioRenderer


@pytest.fixture
def url():
    return 'http://osf.io/file/audio.mp3'


@pytest.fixture
def download_url():
    return 'http://wb.osf.io/file/audio.mp3?token=1234'


@pytest.fixture
def file_path():
    return '/tmp/audio.mp3'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def extension():
    return '.mp3'


@pytest.fixture
def renderer(url, download_url, file_path, assets_url, extension):
    return AudioRenderer(url, download_url, file_path, assets_url, extension)


class TestRenderAudio:

    def test_render_audio(self, renderer, url):
        body = renderer.render()
        assert '<audio controls>' in body
        assert 'src="{}"'.format(url) in body

    def test_render_audio_file_required(self, renderer):
        assert renderer.file_required is False

    def test_render_audio_cache_result(self, renderer):
        assert renderer.cache_result is False
