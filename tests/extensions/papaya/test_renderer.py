import pytest

from mfr.core.provider import ProviderMetadata

from mfr.extensions.papaya import PapayaRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test.nii', '.gz', 'text/plain', '1234', 'http://wb.osf.io/file/test.nii.gz?token=1234')


@pytest.fixture
def file_path():
    return './tests/extensions/papaya/files/507643e2-c0fb-45e4-805e-96231c8251de'


@pytest.fixture
def url():
    return 'http://osf.io/file/test.nii.gz'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, file_path, url, assets_url, export_url):
    return PapayaRenderer(metadata, file_path, url, assets_url, export_url)


class TestPapayaRenderer:

    def test_render_papaya(self, renderer, metadata, assets_url):
        body = renderer.render()
        print(body)
        assert '<script type="text/javascript" src="http://mfr.osf.io/assets/papaya/papaya.js"></script>' in body
        assert 'params["images"] = ["http://mfr.osf.io/assets/papaya/data/507643e2-c0fb-45e4-805e-96231c8251de.nii.gz"]' in body
        assert '<div class="papaya" data-params="params"></div>' in body
