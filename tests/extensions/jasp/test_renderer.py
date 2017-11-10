
import os
import pytest

from mfr.core.provider import ProviderMetadata
from mfr.core.exceptions import RendererError
from mfr.extensions.jasp import JASPRenderer

@pytest.fixture
def metadata():
    return ProviderMetadata('JASP', '.jasp', 'application/octet-stream', '1234', 'http://wb.osf.io/file/JASP.jasp?token=1234')

@pytest.fixture
def ok_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'ok.jasp')

@pytest.fixture
def not_a_zip_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'not-a-zip-file.jasp')

@pytest.fixture
def no_manifest_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'no-manifest.jasp')

@pytest.fixture
def no_data_archive_version_in_manifest_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'no-data-archive-version-in-manifest.jasp')

@pytest.fixture
def data_archive_version_is_too_old_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'data-archive-version-is-too-old.jasp')

@pytest.fixture
def no_index_html_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'no-index_html.jasp')

@pytest.fixture
def contains_malicious_script_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'contains-malicious-script.jasp')


@pytest.fixture
def url():
    return 'http://wb.osf.io/file/JASP.jasp'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def extension():
    return '.jasp'


@pytest.fixture
def renderer(metadata, ok_path, url, assets_url, export_url):
    return JASPRenderer(metadata, ok_path, url, assets_url, export_url)


class TestCodeJASPRenderer:

    def test_render_JASP(self, renderer):
        body = renderer.render()
        assert '<div style="word-wrap: break-word; overflow: auto" class="mfrViewer">' in body

    def test_render_JASP_not_a_zip_file(self, metadata, not_a_zip_file_path, url, assets_url, export_url):
        try:
            renderer = JASPRenderer(metadata, not_a_zip_file_path, url, assets_url, export_url)
            renderer.render()
        except RendererError:
            return

        assert False # should not get here

    def test_render_JASP_no_manifest(self, metadata, no_manifest_path, url, assets_url, export_url):
        try:
            renderer = JASPRenderer(metadata, no_manifest_path, url, assets_url, export_url)
            renderer.render()
        except RendererError:
            return

        assert False # should not get here

    def test_render_JASP_no_data_archive_version_in_manifest(self, metadata, no_data_archive_version_in_manifest_path, url, assets_url, export_url):
        try:
            renderer = JASPRenderer(metadata, no_data_archive_version_in_manifest_path, url, assets_url, export_url)
            renderer.render()
        except RendererError:
            return

        assert False # should not get here

    def test_render_JASP_data_archive_is_too_old(self, metadata, data_archive_version_is_too_old_path, url, assets_url, export_url):
        try:
            renderer = JASPRenderer(metadata, data_archive_version_is_too_old_path, url, assets_url, export_url)
            renderer.render()
        except RendererError:
            return

        assert False # should not get here

    def test_render_JASP_no_index_html(self, metadata, no_index_html_path, url, assets_url, export_url):
        try:
            renderer = JASPRenderer(metadata, no_index_html_path, url, assets_url, export_url)
            renderer.render()
        except RendererError:
            return

        assert False # should not get here

    def test_render_JASP_contains_malicious_script(self, metadata, contains_malicious_script_path, url, assets_url, export_url):
        renderer = JASPRenderer(metadata, contains_malicious_script_path, url, assets_url, export_url)
        body = renderer.render()

        assert '<script src="link-to-something-malicious.js">' not in body
  

    def test_render_JASP_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_JASP_cache_result(self, renderer):
        assert renderer.cache_result is True


