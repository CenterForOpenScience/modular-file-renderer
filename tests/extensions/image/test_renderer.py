import pytest

import furl

from mfr.core.provider import ProviderMetadata

from mfr.extensions.image import ImageRenderer
from mfr.extensions.image import settings


class TestImageRenderer:

    def test_render_image_no_export(self):
        settings.EXPORT_TYPE_MAP = {}
        settings.EXPORT_MAXIMUM_SIZE = None
        settings.EXPORT_TYPE = None

        url = 'http://osf.io/file/test.png'

        metadata = ProviderMetadata('test', '.png', 'text/plain', '1234', 'http://wb.osf.io/file/test.png?token=1234')
        renderer = ImageRenderer(metadata, '/tmp/test.png', url, 'http://mfr.osf.io/assets', 'http://this_should_be_ignored')

        body = renderer.render()

        assert '<img id="base-image" style="max-width: 100%" class="baseImage" src="{}">'.format(url) in body

    def test_render_image_export_type(self):
        settings.EXPORT_TYPE_MAP = {}
        settings.EXPORT_MAXIMUM_SIZE = None
        settings.EXPORT_TYPE = 'fake_type'

        url = 'http://osf.io/file/test.png'
        export_url = furl.furl('http://mfr.osf.io/export')
        export_url.args['url'] = url

        metadata = ProviderMetadata('test', '.png', 'text/plain', '1234', 'http://wb.osf.io/file/test.png?token=1234')
        renderer = ImageRenderer(metadata, '/tmp/test.png', url, 'http://mfr.osf.io/assets', export_url.url)

        exported_url = furl.furl(export_url.url)
        exported_url.args['format'] = settings.EXPORT_TYPE

        body = renderer.render()

        assert '<img id="base-image" style="max-width: 100%" class="baseImage" src="{}">'.format(exported_url) in body

    def test_render_image_export_size_and_type(self):
        settings.EXPORT_TYPE_MAP = {}
        settings.EXPORT_MAXIMUM_SIZE = '1234x4321'
        settings.EXPORT_TYPE = 'fake_type'

        url = 'http://osf.io/file/test.png'
        export_url = furl.furl('http://mfr.osf.io/export')
        export_url.args['url'] = url

        metadata = ProviderMetadata('test', '.png', 'text/plain', '1234', 'http://wb.osf.io/file/test.png?token=1234')
        renderer = ImageRenderer(metadata, '/tmp/test.png', url, 'http://mfr.osf.io/assets', export_url.url)

        exported_url = furl.furl(export_url.url)
        exported_url.args['format'] = '{}.{}'.format(settings.EXPORT_MAXIMUM_SIZE, settings.EXPORT_TYPE)

        body = renderer.render()

        assert '<img id="base-image" style="max-width: 100%" class="baseImage" src="{}">'.format(exported_url) in body

    def test_render_image_excluded_export_file_type(self):
        settings.EXPORT_EXCLUSIONS = ['.png']
        settings.EXPORT_MAXIMUM_SIZE = None
        settings.EXPORT_TYPE = 'fake_type'

        url = 'http://osf.io/file/test.png'

        metadata = ProviderMetadata('test', '.png', 'text/plain', '1234', 'http://wb.osf.io/file/test.png?token=1234')
        renderer = ImageRenderer(metadata, '/tmp/test.png', url, 'http://mfr.osf.io/assets', 'http://this_should_be_ignored')

        body = renderer.render()

        assert '<img id="base-image" style="max-width: 100%" class="baseImage" src="{}">'.format(url) in body

    def test_render_image_export_maximum(self):
        settings.EXPORT_EXCLUSIONS = ['.png']
        settings.EXPORT_MAXIMUM_SIZE = '1234x4321'
        settings.EXPORT_TYPE = 'fake_type'

        url = 'http://osf.io/file/test.png'

        metadata = ProviderMetadata('test', '.png', 'text/plain', '1234', 'http://wb.osf.io/file/test.png?token=1234')
        renderer = ImageRenderer(metadata, '/tmp/test.png', url, 'http://mfr.osf.io/assets', 'http://this_should_be_ignored')

        body = renderer.render()

        assert '<img id="base-image" style="max-width: 100%" class="baseImage" src="{}">'.format(url) in body
