import pytest

from mfr.core.provider import ProviderMetadata
from mfr.extensions.papaya import PapayaRenderer

@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url='


@pytest.fixture
def test_file_dir():
    return './tests/extensions/papaya/files/'


@pytest.fixture
def url():
    return 'http://osf.io/file/test'


valid_render_data = [(ProviderMetadata('test.nii', '.gz', 'text/plain', '1234',
                                       'http://wb.osf.io/file/test.nii.gz?token=1234'),
                      '507643e2-c0fb-45e4-805e-96231c8251de',
                      '.nii.gz'
                     ),
                     (ProviderMetadata('test', '.nii', 'text/plain', '1234',
                                       'http://wb.osf.io/file/test.nii?to  ken=1234'),
                      '298783da-64b0-44e0-bab6-5716ecb9535d',
                      '.nii'
                     ),
                     (ProviderMetadata('test', '.dcm', 'text/plain', '1234',
                                       'http://wb.osf.io/file/test.dcm?to  ken=1234'),
                      'b24a0d9f-c38a-42bd-a2e7-5448d3ce0060',
                      '.dcm'
                     )]


@pytest.fixture(params=valid_render_data)
def valid_renderer(request, assets_url, export_url, test_file_dir, url):
    metadata, file_name, file_ext = request.param
    return PapayaRenderer(metadata, test_file_dir + file_name, url, assets_url,
            export_url + url + file_ext), file_name, file_ext


class TestPapayaRenderer:

    def test_render_papaya_valid(self, valid_renderer):
        renderer, file_name, file_ext = valid_renderer
        body = renderer.render()
        assert '<script type="text/javascript" src="http://mfr.osf.io/assets/papaya/papaya.js"></script>' in body
        assert 'params["images"] = ["http://mfr.osf.io/assets/papaya/data/{}{}"]'.format(file_name, file_ext) in body
        assert '<div class="papaya" data-params="params"></div>' in body
