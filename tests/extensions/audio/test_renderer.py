import pytest

from mfr.core.provider import ProviderMetadata

from mfr.extensions.audio import AudioRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.mp3', 'text/plain', '1234', 'http://wb.osf.io/file/test.mp3?token=1234')


@pytest.fixture
def file_path():
    return '/tmp/test.mp3'


@pytest.fixture
def url():
    return 'http://osf.io/file/test.mp3'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, file_path, url, assets_url, export_url):
    return AudioRenderer(metadata, file_path, url, assets_url, export_url)


class TestAudioRenderer:

    def test_render_audio(self, renderer, url):
        body = renderer.render()
        assert '<audio controls>' in body
        assert 'src="{}"'.format(url) in body

    def test_render_audio_file_required(self, renderer):
        assert renderer.file_required is False

    def test_render_audio_cache_result(self, renderer):
        assert renderer.cache_result is False
