from PIL import Image

from mfr.core import extension
from mfr.core import exceptions


class ImageExporter(extension.BaseExporter):

    def export(self):
        # Pillow will not recognize the jpg extension
        format = 'jpeg' if self.format.lower() == 'jpg' else self.format
        try:
            image = Image.open(self.source_file_path)
            image.save(self.output_file_path, format=format)
        except UnicodeDecodeError:
            raise exceptions.ExporterError('Unable to export the file in the requested format, please try again later.', code=400)
