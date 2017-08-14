import os

import imghdr
from PIL import Image

from reportlab.pdfgen import canvas

from mfr.core import extension
from mfr.extensions.pdf import exceptions


class PdfExporter(extension.BaseExporter):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.metrics.add('pil_version', Image.VERSION)

    def tiff_to_pdf(self, tiff_img, max_size):
        max_pages = 40
        width, height = tiff_img.size
        c = canvas.Canvas(self.output_file_path)
        c.setPageSize((max_size[0], max_size[1]))

        page = 0

        # This seems to be the only way to write this loop at the moment
        while True:
            try:
                tiff_img.seek(page)
            except EOFError:
                break

            # Center the image and draw it in the canvas
            c.drawInlineImage(tiff_img, (max_size[0] - width) // 2, (max_size[1] - height) // 2, anchor='c')
            # move to the next page
            c.showPage()

            if max_pages and page > max_pages:
                break
            page += 1

        c.save()

    def export(self):
        parts = self.format.split('.')
        type = parts[-1].lower()
        max_size = [int(x) for x in parts[0].split('x')] if len(parts) == 2 else None

        self.metrics.merge({
            'type': type,
            'max_size_w': max_size[0],
            'max_size_h': max_size[1],
        })
        try:
            image = Image.open(self.source_file_path)
            if max_size:
                # resize the image to the w/h maximum specified
                ratio = min(max_size[0] / image.size[0], max_size[1] / image.size[1])
                self.metrics.add('ratio', ratio)
                if ratio < 1:
                    image = image.resize((round(image.size[0] * ratio), round(image.size[1] * ratio)), Image.ANTIALIAS)

            self.tiff_to_pdf(image, max_size)
            image.close()

        except (UnicodeDecodeError, IOError) as err:
            name, extension = os.path.splitext(os.path.split(self.source_file_path)[-1])
            raise exceptions.PillowImageError(
                'Unable to export the file as a {}, please check that the '
                'file is a valid image.'.format(type),
                export_format=type,
                detected_format=imghdr.what(self.source_file_path),
                original_exception=err,
                code=400,
            )
        except(ValueError) as err:
            name, extension = os.path.splitext(os.path.split(self.source_file_path)[-1])
            raise exceptions.PillowImageError(
                'Unable to open file. Please check that it is a valid tiff file',
                export_format=type,
                detected_format=imghdr.what(self.source_file_path),
                original_exception=err,
                code=400,
            )
