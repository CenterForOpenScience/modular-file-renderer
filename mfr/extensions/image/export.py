from PIL import Image

from mfr.core import extension


class ImageExporter(extension.BaseExporter):

    def export(self):
        # return '<img src="{src}" />'.format(src=self.url)
        try:
            with open(self.file_path, 'w') as fp:
                image = Image.open(fp)
                image.save(self.dest_file, format=self.export_ext)
        except UnicodeDecodeError as e:
            return "Unable to export: {0}".format(e)
