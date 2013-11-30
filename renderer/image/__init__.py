from .. import FileRenderer
from cStringIO import StringIO
import Image
import os
from flask import request
from PIL import Image
from flask import redirect


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
        img =  '''
           <br></br><br></br>
           <img src='%s'%s id='target'/>
            ''' % (path, style)
        return img

    def edit(self, fp, path):
        filename = str(os.path.split(fp.name)[1])
        html_from_file = open(os.getcwd() + "/renderer/image/jcrop.html").read()
        html_with_data = html_from_file % (path, filename)
        return html_with_data

    def save(self, fp, path):
        filename = str(os.path.split(fp.name)[1])
        filepath = os.path.join('examples', filename)
        box = (int(request.form['x1']), int(request.form['y1']),
               int(request.form['x2']), int(request.form['y2']))
        img = Image.open(filepath)
        width, height = img.size
        if width > 600 or height > 600:
            multiplier = 600.0/max(height, width)
            box = [int(x/multiplier) for x in box]
        img.crop(box).save(filepath)
        return redirect('/render/{}'.format(filename))




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

    def export_edit(self,fp):
        return fp.read(), 'edit'
