from .. import FileRenderer
from cStringIO import StringIO
from PIL import Image

class ImageRenderer(FileRenderer):

    def __init__(self, max_width=None):
        self.max_width = max_width

    def detect(self, fp):
        fname = fp.name
        for ext in ['jpg', 'gif', 'tiff', 'png']:
            if fname.endswith(ext):
                return ext
     	return ''

    def render(self, fp, path):
        if self.max_width:
            style = ' style="max-width: {}"'.format(self.max_width)
        else:
            style = ''
        return '<img src="{}"{} />'.format(path, style)

    def export_gif(self, fp):
        im = Image.open(fp)
        sio = StringIO()
        im.save(sio, format='gif')
        return sio.getvalue(), '.gif'

    def export_tiff(self, fp):
        im = Image.open(fp)
        sio = StringIO()
        im.save(sio, format='tiff')
        return sio.getvalue(), '.tiff'

    def export_png(self, fp):
	im = Image.open(fp)
        sio = StringIO()
        im.save(sio, format='png')
        return sio.getvalue(), '.png'

    def export_jpg(self, fp):
        im = Image.open(fp)
        sio = StringIO()
        im.save(sio, format='jpg')
        return sio.getvalue(), '.jpg'