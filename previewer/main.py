# -*- coding: utf-8 -*-
"""Flask app for previewing files.
"""

import os
from urllib import quote
from flask import Flask, send_file, send_from_directory, url_for
from cStringIO import StringIO
import mfr
import logging

logger = logging.getLogger(__name__)
HERE = os.path.abspath(os.path.dirname(__file__))
FILES_DIR = os.path.join(HERE, 'files')

# TODO(sloria): For now, filehandlers are registered manually. Once the configuration
# system is in place use a proper config file to define which handlers should be used
# and remove this code.
from mfr.image.handler import ImageFileHandler
mfr.register_filehandler('image', ImageFileHandler)

from mfr.docx.handler import DocxFileHandler
mfr.register_filehandler('docx', DocxFileHandler)

#todo(ajs) fix this stupid way of doing ALL the try/excepts
# module imports
try:
    from mfr.rst.handler import RstFileHandler
    mfr.register_filehandler('rst', RstFileHandler)
except Exception as error:
    logging.error(error)

from mfr.code.handler import CodeFileHandler
mfr.register_filehandler('code', CodeFileHandler)


### html building helpers

def build_export_html(file_name, handler):
    html = ''
    exporters = mfr.get_file_exporters(handler)
    if exporters:
        html += "</br><span style='margin-left:20px;'> export to: </span>"
        for exporter in exporters:
            html += '<a href="/export/{exporter}/{file_name}"> {exporter}, </a>'.format(
                exporter=exporter,
                file_name=file_name)
    return html

# TODO(sloria): Put in template
def build_html(file_name):
    html = ''
    if file_name[0] != ".": # gets rid of .DSStore and .gitignore
        fp = open(os.path.join(FILES_DIR, file_name))
        handler = mfr.detect(fp)
        if handler:
            html += '<a href="/render/{safe_name}">{file_name} </a>'.format(
                safe_name=quote(file_name),
                file_name=file_name)
            html += build_export_html(file_name, handler)
        else:
            html += '<span>' + file_name + "</span>"
        html += "</br></br>"
    return html

## App Start ##

app = Flask(__name__, static_folder='files')

@app.route('/')
def index():
    html = 'Below are files in the modular-file-renderer/previewer/files folder. Click-able links are those that the renderer can detect.</br>'
    for file_name in os.listdir(FILES_DIR):
        html += build_html(file_name)
    return html


@app.route('/render/<file_name>')
def render(file_name):
    fp = open(os.path.join(FILES_DIR, file_name))
    handler = mfr.detect(fp)
    if handler:
        try:
            return mfr.render(fp, handler,
                src=url_for('static', filename=file_name))
        except Exception as err:
            return err.message
    return 'Cannot render {file_name}.'.format(file_name=file_name)

@app.route('/export/<exporter>/<file_name>')
def export(exporter, file_name):
    fp = open(os.path.join(FILES_DIR, file_name))
    handler = mfr.detect(fp)
    exp = mfr.export(fp, handler, exporter="png")
    short_name, _ = os.path.splitext(file_name)
    export_name = short_name + '.' + exporter
    return send_file(
        StringIO(exp),
        as_attachment=True,
        attachment_filename=export_name,
    )

@app.route('/render/static/<module>/<path:file_path>')
def send_module_file(module, file_path):
    file_path, file_name = os.path.split(file_path)
    module_static_dir = os.path.join('..', 'mfr', module, 'static', file_path)
    return send_from_directory(module_static_dir, file_name)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
