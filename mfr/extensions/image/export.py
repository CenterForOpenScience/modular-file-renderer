from PIL import Image

from mfr.core import extension
from mfr.core import exceptions


class ImageExporter(extension.BaseExporter):

    def export(self):
        try:
            image = Image.open(self.source_file_path)
            image.save(self.output_file_path)
        except UnicodeDecodeError:
            raise exceptions.ExporterError('Unable to export the file in the requested format, please try again later.', code=400)
