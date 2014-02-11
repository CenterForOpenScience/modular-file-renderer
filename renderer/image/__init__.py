from .. import FileRenderer
from cStringIO import StringIO
from PIL import Image
import os
from flask import request, redirect
import imghdr
import base64


import logging
logging.basicConfig(level=logging.DEBUG)


class ImageRenderer(FileRenderer):

    # Override superclass MAX_SIZE
    def __init__(self, max_width=None):
        self.max_width = max_width

    def _detect(self, file_pointer):
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

    def _render(self, file_pointer, **kwargs):
        url = kwargs['url']
        img = '''
           <img src='%s' id='target'/>
            ''' % (url)
        return img

    def _edit(self, file_pointer, **kwargs):
        _, file_name = os.path.split(file_pointer.name)
        html_from_file = open(os.getcwd() +
                              #"/renderer/image/static/Jcrop/html/jcrop.html").read()
                              "/renderer/image/static/canvas/html/edit.html").read()

        html_with_data = html_from_file % (file_path, imghdr.what(file_pointer), file_name)
        return html_with_data


    def _save(self, file_pointer, **kwargs):
        _, file_name = os.path.split(file_pointer.name)
        file_path = os.path.join('examples', file_name)
        image_data = request.form['imageData']
        _, b64_image_data = image_data.split('base64,')
        binary_image_data = base64.b64decode(b64_image_data)
        f = open(file_path, 'wb')
        f.write(binary_image_data)
        f.close()
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
