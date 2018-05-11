import asyncio
import imghdr
from os.path import (
    basename,
    splitext
)
import warnings

from PIL import Image
from psd_tools import PSDImage

from mfr.core import extension
from mfr.extensions.image import exceptions
from mfr.extensions.image.settings import EXPORT_BACKGROUND_COLOR


class ImageExporter(extension.BaseExporter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics.add('pil_version', Image.VERSION)

    async def export(self):
        parts = self.format.split('.')
        self.filetype = parts[-1].lower()
        self.max_size = [int(x) for x in parts[0].split('x')] if len(parts) == 2 else None
        self.metrics.merge({
            'type': type,
            'max_size_w': self.max_size[0],
            'max_size_h': self.max_size[1],
        })
        source_file_path = await self.source_file_path
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.resize(source_file_path)
        )

    def resize(self, source_file_path):
        try:
            if self.ext in ['.psd']:
                # silence warnings from psd-tools
                # Warnings warn of outdated depedency that is a pain to install
                # and about colors being possibly wrong
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    image = PSDImage.load(source_file_path).as_PIL()
            else:
                image = Image.open(source_file_path)

            if self.max_size:
                # resize the image to the w/h maximum specified
                ratio = min(self.max_size[0] / image.size[0], self.max_size[1] / image.size[1])
                self.metrics.add('ratio', ratio)
                if ratio < 1:
                    image = image.resize(
                        (round(image.size[0] * ratio), round(image.size[1] * ratio)),
                        Image.ANTIALIAS
                    )

            # handle transparency
            # from https://github.com/python-pillow/Pillow/issues/2609
            if image.mode in ('RGBA', 'RGBa', 'LA') and self.filetype in ['jpeg', 'jpg']:
                # JPEG has no transparency, so anything that was transparent gets changed to
                # EXPORT_BACKGROUND_COLOR. Default is white.
                background = Image.new(image.mode[:-1], image.size, EXPORT_BACKGROUND_COLOR)
                background.paste(image, image.split()[-1])
                image = background

            image.save(self.output_file_path, self.filetype)
            image.close()

        except (UnicodeDecodeError, IOError, FileNotFoundError, OSError) as err:
            name, extension = splitext(basename(getattr(self, '_source_file_path', '')))
            raise exceptions.PillowImageError(
                'Unable to export the file as a {}, please check that the '
                'file is a valid image.'.format(self.filetype),
                export_format=self.filetype,
                detected_format=imghdr.what(getattr(self, '_source_file_path', '')),
                original_exception=err,
                code=400,
            )
