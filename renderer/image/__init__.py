from .. import FileRenderer
from cStringIO import StringIO
from PIL import Image
import os
from flask import request, redirect
import imghdr


import logging
logging.basicConfig(level=logging.DEBUG)


class ImageRenderer(FileRenderer):

    # Override superclass MAX_SIZE
    def __init__(self, max_width=None):
        self.max_width = max_width

    def detect(self, file_pointer):
        """Detects whether a given file pointer can be rendered by
        this renderer. Checks both the extension in list and the file encoding
        using the imghdr lib

        :param file_pointer: File pointer
        :return: Can file be rendered? (bool)

        """
        _, file_name = os.path.split(file_pointer.name)
        for ext in ['.jpeg', '.jpg', '.png', '.tiff', '.bmp', '.tif']:
            if file_pointer.name.endswith(ext):
                header_type = imghdr.what(file_pointer)
                if type is None:
                    return False
                file_type = "." + header_type
                for ext in ['.jpeg', '.jpg', '.png', '.tiff', '.bmp', '.tif']:
                    if file_type == ext:
                        return True
        return False

    def render(self, file_pointer, file_path):
        if self.max_width:


            style = 'style="max-width: {}"'.format(self.max_width)
        else:
            style = ''
        img = '''
           <br></br><br></br>
           <img src='%s'%s id='target'/>
            ''' % (file_path, style)
        return img

    def edit(self, file_pointer, file_path):
        _, file_name = os.path.split(file_pointer.name)
        html_from_file = open(os.getcwd() +
                              "/renderer/image/static/jcrop/html/jcrop.html").read()
        html_with_data = html_from_file % (file_path, file_name)
        return html_with_data

    def save(self, file_pointer, file_path):
        _, file_name = os.path.split(file_pointer.name)
        file_path = os.path.join('examples', file_name)
        box = (int(request.form['x1']), int(request.form['y1']),
               int(request.form['x2']), int(request.form['y2']))
        img = Image.open(file_path)
        width, height = img.size
        if width > 600 or height > 600:
            multiplier = 600.0 / max(height, width)
            box = [int(x / multiplier) for x in box]
        img.crop(box).save(file_path)
        return redirect('/render/{}'.format(file_name))

    def export_gif(self, file_pointer):
        im = Image.open(file_pointer)
        sio = StringIO()
        im.save(sio, format='gif')
        return sio.getvalue(), '.gif'

    def export_tiff(self, file_pointer):
        im = Image.open(file_pointer)
        sio = StringIO()
        im.save(sio, format='tiff')
        return sio.getvalue(), '.tiff'

    def export_edit(self, file_pointer):
        return file_pointer.read(), 'edit'
