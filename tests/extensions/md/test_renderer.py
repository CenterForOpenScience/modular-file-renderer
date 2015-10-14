import os
import pytest

from mfr.core.provider import ProviderMetadata
from mfr.extensions.md import MdRenderer


@pytest.fixture
def metadata():
    return ProviderMetadata('test', '.md', 'text/plain', '1234', 'http://wb.osf.io/file/test.md?token=1234')


@pytest.fixture
def test_md_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'test.md')


@pytest.fixture
def invalid_md_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'invalid.md')

@pytest.fixture
def url():
    return 'http://osf.io/file/test.md'


@pytest.fixture
def assets_url():
    return 'http://mfr.osf.io/assets'


@pytest.fixture
def export_url():
    return 'http://mfr.osf.io/export?url=' + url()


@pytest.fixture
def renderer(metadata, test_md_file_path, url, assets_url, export_url):
    return MdRenderer(metadata, test_md_file_path, url, assets_url, export_url)


class TestMdRenderer:

    def test_render_md_file_required(self, renderer):
        assert renderer.file_required is True

    def test_render_md_cache_result(self, renderer):
        assert renderer.cache_result is True

    def test_render_md(self, test_md_file_path, assets_url, export_url):
        metadata = ProviderMetadata('test', '.md', 'text/plain', '1234', 'http://wb.osf.io/file/test.md?token=1234')
        renderer = MdRenderer(metadata, test_md_file_path, url, assets_url, export_url)
        body = renderer.render()
        inbody = """
<h1>Heading</h1>
<h2>Sub-heading</h2>
<h3>Another deeper heading</h3>
<p>Paragraphs are separated
by a blank line.</p>
<p>Leave 2 spaces at the end of a line to do a<br />
line break</p>
<p>Text attributes <em>italic</em>, <strong>bold</strong>, 
<code>monospace</code>.</p>
<p>A <a href="http://example.com">link</a>.
[28]</p>
<p>Shopping list:</p>
<ul>
<li>apples</li>
<li>oranges</li>
<li>pears</li>
</ul>
<p>Numbered list:</p>
<ol>
<li>apples</li>
<li>oranges</li>
<li>pears</li>
</ol>
<p>The rain---not the reign---in
Spain.</p>
<p>&lt;script&gt;
alert("Hello world");
&lt;/script&gt;</p>
"""
        assert inbody in body

