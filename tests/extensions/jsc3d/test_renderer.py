import pytest

from mfr.core.provider import ProviderMetadata

from mfr.extensions.jsc3d import JSC3DRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.stl', 'text/plain', '1234', 'http://wb.osf.io/file/test.stl?token=1234')


@pytest.fixture
def file_path():
    return '/tmp/test.stl'


@pytest.fixture
def url():
    return 'http://osf.io/file/test.stl'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, file_path, url, assets_url, export_url):
    return JSC3DRenderer(metadata, file_path, url, assets_url, export_url)


class TestPdbRenderer:

    def test_render_stl(self, renderer):
        body = renderer.render()
        assert '<canvas id="mfrViewer"></canvas>' in body
        assert 'viewer.init();' in body
