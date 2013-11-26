from .. import FileRenderer
from cStringIO import StringIO
import Image


class ImageRenderer(FileRenderer):

    def __init__(self, max_width=None):
        self.max_width = max_width

    def detect(self, fp):
        fname = fp.name
        for ext in ['jpg', 'png', 'tif']:
            if fname.endswith(ext):
                return True
        return False

    def render(self, fp, path):
        fname = fp.name
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