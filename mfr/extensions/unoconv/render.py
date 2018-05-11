import os

import furl

from mfr.core import (
    utils,
    extension
)

from mfr.extensions.unoconv import settings


class UnoconvRenderer(extension.BaseRenderer):

    def __init__(self, metadata, file_stream, url, assets_url, export_url):
        super().__init__(metadata, file_stream, url, assets_url, export_url)

        try:
            self.map = settings.RENDER_MAP[self.metadata.ext]
        except KeyError:
            self.map = settings.DEFAULT_RENDER

        # can't call file_required until renderer is built
        self.renderer_metrics.add('file_required', self.file_required)
        self.renderer_metrics.add('cache_result', self.cache_result)

        self.metrics.merge({
            'map': {
                'renderer': self.map['renderer'],
                'format': self.map['format'],
            },
        })

    async def get_export_file_path(self):
        return (await self.get_source_file_path()).fullpath + self.map['renderer']

    file_converted = None

    @property
    def input_file(self):
        if not self.file_converted:
            exporter = utils.make_exporter(
                self.metadata.ext,
                self.file_path,
                self.export_file_path,
                self.map['format']
            )
            exporter.export()
            self.file_converted = True
        return

    @property
    def exported_metadata(self):
        exported_metadata = self.metadata
        exported_metadata.download_url = self.exported_url.url
        return exported_metadata

    @property
    def exported_url(self):
        exported_url = furl.furl(self.export_url)
        exported_url.args['format'] = self.map['format']
        return exported_url

    def render(self):

        rendition = self.renderer.render()
        self.metrics.add('subrenderer', self.renderer.renderer_metrics.serialize())

        if self.renderer.file_required:
            try:
                os.remove(self.export_file_path)
            except FileNotFoundError:
                pass

        return rendition

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return True
