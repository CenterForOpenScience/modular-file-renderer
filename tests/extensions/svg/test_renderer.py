import os
import pytest

from mfr.core.provider import ProviderMetadata

from mfr.extensions.svg import SvgRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.rst', 'text/plain', '1234', 'http://wb.osf.io/file/test.svg?token=1234')


@pytest.fixture
def test_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.svg')


@pytest.fixture
def url():
    return 'http://osf.io/file/test.svg'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, test_file_path, url, assets_url, export_url):
    return SvgRenderer(metadata, test_file_path, url, assets_url, export_url)


class TestSvgRenderer:

    def test_render_svg(self, renderer):
        body = renderer.render()
        assert """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="pyYellow" gradientTransform="rotate(45)">
      <stop stop-color="#fe5" offset="0.6"/>
      <stop stop-color="#da1" offset="1"/>
    </linearGradient>
    <linearGradient id="pyBlue" gradientTransform="rotate(45)">
      <stop stop-color="#69f" offset="0.4"/>
      <stop stop-color="#468" offset="1"/>
    </linearGradient>
  </defs>

  <path d="M27,16c0-7,9-13,24-13c15,0,23,6,23,13l0,22c0,7-5,12-11,12l-24,0c-8,0-14,6-14,15l0,10l-9,0c-8,0-13-9-13-24c0-14,5-23,13-23l35,0l0-3l-24,0l0-9l0,0z M88,50v1" fill="url(#pyBlue)"/>
  <path d="M74,87c0,7-8,13-23,13c-15,0-24-6-24-13l0-22c0-7,6-12,12-12l24,0c8,0,14-7,14-15l0-10l9,0c7,0,13,9,13,23c0,15-6,24-13,24l-35,0l0,3l23,0l0,9l0,0z M140,50v1" fill="url(#pyYellow)"/>

  <circle r="4" cx="64" cy="88" fill="#FFF"/>
  <circle r="4" cx="37" cy="15" fill="#FFF"/>
</svg>""" in body

    def test_render_svg_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_svg_cache_result(self, renderer):
        assert renderer.cache_result is False
