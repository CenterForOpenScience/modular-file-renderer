import os

from mfr.core import utils
from mfr.core import extension
from mfr.core import exceptions

from mfr.extensions.unoconv import settings


class UnoconvRenderer(extension.BaseRenderer):

    def __init__(self, metadata, url, file_path, assets_url):
        super().__init__(metadata, url, file_path, assets_url)
        self.export_url = self.url + 'export'  # FIX

    def render(self):
        try:
            map = settings.RENDER_MAP[self.metadata.ext]
        except KeyError:
            raise exceptions.RendererError('No renderer could be found for the file type requested.', code=400)

        export_metadata = self.metadata
        export_metadata.download_url = self.export_url
        export_file_path = self.file_path + map['renderer']

        self.renderer = utils.make_renderer(
            map['renderer'],
            export_metadata,
            self.url,
            export_file_path,
            self.assets_url
        )

        self.exporter = utils.make_exporter(
            map['renderer'],
            export_metadata,
            self.file_path,
            export_file_path,
            map['format']
        )

        if self.renderer.file_required:
            self.exporter.export()

        rendition = self.renderer.render()

        if self.renderer.file_required:
            try:
                os.remove(export_file_path)
            except FileNotFoundError:
                pass

        return rendition

    @property
    def file_required(self):
        # Always false, if we do require the file we will download it in its exported final format.
        return False

    @property
    def cache_result(self):
        return self.renderer.cache_result
