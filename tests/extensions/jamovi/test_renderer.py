
import os
import pytest

from mfr.core.provider import ProviderMetadata
from mfr.core.exceptions import RendererError
from mfr.extensions.jamovi import JamoviRenderer

@pytest.fixture
def metadata():
    return ProviderMetadata('jamovi', '.omv', 'application/octet-stream', '1337', 'http://wb.osf.io/file/jamovi.omv?token=1337')

@pytest.fixture
def ok_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'ok.omv')

@pytest.fixture
def not_a_zip_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'not-a-zip-file.omv')

@pytest.fixture
def no_manifest_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'no-manifest.omv')

@pytest.fixture
def no_data_archive_version_in_manifest_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'no-data-archive-version-in-manifest.omv')

@pytest.fixture
def data_archive_version_is_too_old_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'data-archive-version-is-too-old.omv')

@pytest.fixture
def no_index_html_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'no-index_html.omv')

@pytest.fixture
def contains_malicious_script_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'contains-malicious-script.omv')


@pytest.fixture
def url():
    return 'http://wb.osf.io/file/jamovi.omv'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def extension():
    return '.omv'


@pytest.fixture
def renderer(metadata, ok_path, url, assets_url, export_url):
    return JamoviRenderer(metadata, ok_path, url, assets_url, export_url)


class TestCodeJamoviRenderer:

    def test_render_jamovi(self, renderer):
        body = renderer.render()
        assert '<div style="word-wrap: break-word;" class="mfrViewer">' in body

    def test_render_jamovi_not_a_zip_file(self, metadata, not_a_zip_file_path, url, assets_url, export_url):
        try:
            renderer = JamoviRenderer(metadata, not_a_zip_file_path, url, assets_url, export_url)
            renderer.render()
        except RendererError:
            return

        assert False # should not get here

    def test_render_jamovi_no_manifest(self, metadata, no_manifest_path, url, assets_url, export_url):
        try:
            renderer = JamoviRenderer(metadata, no_manifest_path, url, assets_url, export_url)
            renderer.render()
        except RendererError:
            return

        assert False # should not get here

    def test_render_jamovi_no_data_archive_version_in_manifest(self, metadata, no_data_archive_version_in_manifest_path, url, assets_url, export_url):
        try:
            renderer = JamoviRenderer(metadata, no_data_archive_version_in_manifest_path, url, assets_url, export_url)
            renderer.render()
        except RendererError:
            return

        assert False # should not get here

    def test_render_jamovi_data_archive_is_too_old(self, metadata, data_archive_version_is_too_old_path, url, assets_url, export_url):
        try:
            renderer = JamoviRenderer(metadata, data_archive_version_is_too_old_path, url, assets_url, export_url)
            renderer.render()
        except RendererError:
            return

        assert False # should not get here

    def test_render_jamovi_no_index_html(self, metadata, no_index_html_path, url, assets_url, export_url):
        try:
            renderer = JamoviRenderer(metadata, no_index_html_path, url, assets_url, export_url)
            renderer.render()
        except RendererError:
            return

        assert False # should not get here

    def test_render_jamovi_contains_malicious_script(self, metadata, contains_malicious_script_path, url, assets_url, export_url):
        renderer = JamoviRenderer(metadata, contains_malicious_script_path, url, assets_url, export_url)
        body = renderer.render()

        assert '<script>' not in body


    def test_render_jamovi_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_jamovi_cache_result(self, renderer):
        assert renderer.cache_result is True
