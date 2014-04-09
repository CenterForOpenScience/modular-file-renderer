# -*- coding: utf-8 -*-
"""Flask app for previewing files.
"""

import os
from urllib import quote
from flask import Flask, send_file, send_from_directory, url_for
from cStringIO import StringIO
import logging

import mfr
import mfr_image
import mfr_docx
import mfr_rst
import mfr_code_pygments
from mfr_code_pygments.configuration import config

logger = logging.getLogger(__name__)
HERE = os.path.abspath(os.path.dirname(__file__))
FILES_DIR = os.path.join(HERE, 'files')



### html building helpers

def build_export_html(filename, handler):
    html = ''
    exporters = mfr.get_file_exporters(handler)
    if exporters:
        html += "</br><span style='margin-left:20px;'> export to: </span>"
        for exporter in exporters:
            html += '<a href="/export/{exporter}/{filename}"> {exporter}, </a>'.format(
                exporter=exporter,
                filename=filename)
    return html

# TODO(sloria): Put in template
def build_html(filename):
    html = ''
    if filename[0] != ".": # gets rid of .DSStore and .gitignore
        fp = open(os.path.join(FILES_DIR, filename))
        handler = mfr.detect(fp)
        if handler:
            html += '<a href="/render/{safe_name}">{filename} </a>'.format(
                safe_name=quote(filename),
                filename=filename)
            html += build_export_html(filename, handler)
        else:
            html += '<span>' + filename + "</span>"
        html += "</br></br>"
    return html

## App Start ##

app = Flask(__name__)

# Configure MFR

class MFRConfig:
    # Base URL for static files
    STATIC_URL = app.static_url_path
    # Where to save static files
    STATIC_FOLDER = app.static_folder
    # Allow renderers to include static asset imports
    INCLUDE_STATIC = True

    # Available file handlers
    HANDLERS = [mfr_image.Handler,
                mfr_docx.Handler,
                mfr_rst.Handler,
                mfr_code_pygments.Handler]


class AppConfig:
    # Where the files to render are
    FILES_DIR = FILES_DIR

app.config.from_object(AppConfig)

@app.route('/')
def index():
    html = 'Below are files in the modular-file-renderer/previewer/files folder. Click-able links are those that the renderer can detect.</br>'
    for filename in os.listdir(FILES_DIR):
        html += build_html(filename)
    return html


@app.route('/render/<filename>')
def render(filename):
    fp = open(os.path.join(FILES_DIR, filename))
    handler = mfr.detect(fp, many=False)  # return the first valid filehandler
    if handler:
        try:
            src = url_for('serve_file', filename=filename)
            return mfr.render(fp, handler=handler, src=src)
        except Exception as err:
            return err.message
    return 'Cannot render {filename}.'.format(filename=filename)

@app.route('/export/<exporter>/<filename>')
def export(exporter, filename):
    fp = open(os.path.join(FILES_DIR, filename))
    handler = mfr.detect(fp)
    exp = mfr.export(fp, handler, exporter="png")
    short_name, _ = os.path.splitext(filename)
    export_name = short_name + '.' + exporter
    return send_file(
        StringIO(exp),
        as_attachment=True,
        attachment_filename=export_name,
    )


@app.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['FILES_DIR'], filename)


@app.route('/render/static/<module>/<path:file_path>')
def send_module_file(module, file_path):
    file_path, filename = os.path.split(file_path)
    module_static_dir = os.path.join('..', 'mfr', module, 'static', file_path)
    return send_from_directory(module_static_dir, filename)


def main(*args, **kwargs):
    """Run the app. Takes the same arguments as ``Flask#run``."""
    mfr.config.from_object(MFRConfig)
    mfr.collect_static()
    app.run(*args, **kwargs)

if __name__ == '__main__':
    main()
