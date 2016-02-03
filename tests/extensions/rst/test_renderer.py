import os
import pytest

from mfr.core.provider import ProviderMetadata

from mfr.extensions.rst import RstRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.rst', 'text/plain', '1234', 'http://wb.osf.io/file/test.rst?token=1234')


@pytest.fixture
def test_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.rst')


@pytest.fixture
def invalid_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.rst')


@pytest.fixture
def url():
    return 'http://osf.io/file/test.rst'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, test_file_path, url, assets_url, export_url):
    return RstRenderer(metadata, test_file_path, url, assets_url, export_url)


class TestRstRenderer:

    def test_render_rst(self, renderer):
        body = renderer.render()
        assert """
<h1 class="title">Test</h1>
<p>&lt;script&gt;
alert(&quot;Hello world&quot;);
&lt;/script&gt;</p>
"""  in body

    def test_render_rst_invalid(self, metadata, invalid_file_path, url, assets_url, export_url):
        renderer = RstRenderer(metadata, invalid_file_path, url, assets_url, export_url)
        with pytest.raises(UnicodeDecodeError):
            renderer.render()

    def test_render_rst_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_rst_cache_result(self, renderer):
        assert renderer.cache_result is True
