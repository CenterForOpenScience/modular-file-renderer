# -*- coding: utf-8 -*-
"""Flask app for previewing files.
"""


import os
import random

from urllib import quote
from flask import Flask

import mfr
from mfr.core import register_filehandler

# module imports
from mfr.image.handler import ImageFileHandler

# register module imports
register_filehandler('image', ImageFileHandler)

app = Flask(__name__, static_folder='files')


@app.route('/')
def index():
    html = ''
    for file_name in os.listdir('files'):
        safe_name = quote(file_name)
        html += '<a href="/render/{safe_name}">{file_name}</a><br />'.format(
             safe_name=safe_name, file_name=file_name)
    return html


@app.route('/render/<file_name>')
def render(file_name):
    fp = open(os.path.join('files', file_name))
    renderer = mfr.detect(fp)
    if renderer:
        try:
            return mfr.render(fp, renderer)
        except Exception as err:
            return err.message
    return file_name


if __name__ == '__main__':
    app.run(debug=True, port=5001)