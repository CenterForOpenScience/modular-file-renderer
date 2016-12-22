from PIL import Image
import imghdr

from mfr.core import extension
from mfr.extensions.image import exceptions as image_exceptions


class ImageExporter(extension.BaseExporter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics.add('pil_version', Image.VERSION)

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
            if type in ['jpeg', 'jpg']:
                # handle transparency
                image = image.convert('RGBA')
                exported_image = Image.new("RGBA", image.size, (255, 255, 255))
                exported_image.paste(image, image)
                image.close()
            else:
                exported_image = image
                image.close()
            exported_image.save(self.output_file_path, type)
            exported_image.close()
        except (UnicodeDecodeError, IOError) as err:
            raise image_exceptions.PillowImageError('Unable to export the file in the requested format, please check that file is a valid {}.'.format(type), type, imghdr.what(self.source_file_path), str(err), err.__class__.__name__, self.__class__.__name__, '.{}'.format(type), code=400)
