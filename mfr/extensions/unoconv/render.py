import os

import furl

from mfr.core import utils
from mfr.core import extension
from mfr.core import exceptions

from mfr.extensions.unoconv import settings


class UnoconvRenderer(extension.BaseRenderer):

    def __init__(self, metadata, url, file_path, assets_url):
        super().__init__(metadata, url, file_path, assets_url)
        self.base_assets_url = assets_url

        try:
            map = settings.RENDER_MAP[self.metadata.ext]
        except KeyError:
            raise exceptions.RendererError('No renderer could be found for the file type requested.', code=400)

        self.export_file_path = self.file_path + map['renderer']

        export_url = furl.furl(self.base_assets_url.replace('/assets', '/export'))  # TODO: need to pass proper export url
        export_url.args['url'] = self.url
        export_url.args['format'] = map['format']
        export_metadata = self.metadata
        export_metadata.download_url = export_url.url

        self.renderer = utils.make_renderer(
            map['renderer'],
            self.metadata,
            export_url.url,
            self.export_file_path,
            self.assets_url
        )

        self.exporter = utils.make_exporter(
            self.metadata.ext,
            self.metadata,
            self.file_path,
            self.export_file_path,
            map['format']
        )

    def render(self):
        if self.renderer.file_required:
            self.exporter.export()

        rendition = self.renderer.render()

        if self.renderer.file_required:
            try:
                os.remove(self.export_file_path)
            except FileNotFoundError:
                pass

        return rendition

    @property
    def file_required(self):
        return self.renderer.file_required

    @property
    def cache_result(self):
        return self.renderer.cache_result
