import os
import imghdr
import logging
from http import HTTPStatus

from PIL import Image, TiffImagePlugin
from reportlab.pdfgen import canvas

from mfr.core import extension
from mfr.extensions.pdf import exceptions
from mfr.extensions.pdf.settings import EXPORT_MAX_PAGES

logger = logging.getLogger(__name__)


class PdfExporter(extension.BaseExporter):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.metrics.add('pil_version', Image.VERSION)

    def tiff_to_pdf(self, tiff_img, max_size):
        """ Turn a tiff into a pdf to support multipage tiffs"""

        c = canvas.Canvas(self.output_file_path)
        c.setPageSize((max_size[0], max_size[1]))

        page = 0

        # This seems to be the only way to write this loop at the moment
        while page < EXPORT_MAX_PAGES:
            try:
                tiff_img.seek(page)
            except EOFError:
                break

            # Set the width on each iteration in case its different per page
            width, height = tiff_img.size

            # Use temp_image so we can resize without deleting other images in the tiff file
            temp_image = tiff_img
            # Center the image and draw it in the canvas
            if max_size:

                # Resize the image to the w/h maximum specified
                # This is left in the loop incase images are different sizes.
                ratio = min(max_size[0] / temp_image.size[0], max_size[1] / temp_image.size[1])

                if ratio < 1:
                    temp_image = tiff_img.copy()

                    # Resampling can cause corruption in the image, causing pdf.js errors
                    # Image.ANITALIAS and IMAGE.LANCZOS both caused the error
                    temp_image = temp_image.resize((round(temp_image.size[0] * ratio),
                                                    round(temp_image.size[1] * ratio)),
                                                    Image.BICUBIC)

                    width, height = temp_image.size

            c.drawInlineImage(temp_image, (max_size[0] - width) // 2,
                             (max_size[1] - height) // 2, anchor='c')
            c.showPage()
            page += 1

        c.save()

    def export(self):
        logger.debug('pdf-export: format::{}'.format(self.format))
        parts = self.format.split('.')
        export_type = parts[-1].lower()
        max_size = [int(x) for x in parts[0].split('x')] if len(parts) == 2 else None

        self.metrics.merge({
            'type': export_type,
            'max_size_w': max_size[0],
            'max_size_h': max_size[1],
        })

        try:
            TiffImagePlugin.READ_LIBTIFF = True
            image = Image.open(self.source_file_path)

            if max_size:
                # Done here just for metrics
                ratio = min(max_size[0] / image.size[0], max_size[1] / image.size[1])
                self.metrics.add('ratio', ratio)

            self.tiff_to_pdf(image, max_size)
            image.close()

        except (UnicodeDecodeError, IOError) as err:
            name, extension = os.path.splitext(os.path.split(self.source_file_path)[-1])
            raise exceptions.PillowImageError(
                'Unable to export the file as a {}, please check that the '
                'file is a valid tiff image.'.format(export_type),
                export_format=export_type,
                detected_format=imghdr.what(self.source_file_path),
                original_exception=err,
                code=HTTPStatus.BAD_REQUEST,
            )
