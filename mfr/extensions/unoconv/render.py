import os

import furl

from mfr.core import utils
from mfr.core import extension

from mfr.extensions.unoconv import settings


class UnoconvRenderer(extension.BaseRenderer):

    def __init__(self, metadata, file_path, url, assets_url, export_url):
        super().__init__(metadata, file_path, url, assets_url, export_url)

        try:
            self.map = settings.RENDER_MAP[self.metadata.ext]
        except KeyError:
            self.map = settings.DEFAULT_RENDER

        self.export_file_path = self.file_path + self.map['renderer']

        exported_url = furl.furl(export_url)
        exported_url.args['format'] = self.map['format']
        exported_metadata = self.metadata
        exported_metadata.download_url = exported_url.url

        self.renderer = utils.make_renderer(
            self.map['renderer'],
            exported_metadata,
            self.export_file_path,
            exported_url.url,
            assets_url,
            export_url
        )

    def render(self):
        if self.renderer.file_required:
            exporter = utils.make_exporter(
                self.metadata.ext,
                self.file_path,
                self.export_file_path,
                self.map['format']
            )
            exporter.export()

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
