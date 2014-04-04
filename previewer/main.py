# -*- coding: utf-8 -*-
"""Flask app for previewing files.
"""


import os
import random

from urllib import quote
from flask import Flask, send_file, send_from_directory
from cStringIO import StringIO
import mfr


# module imports
# from mfr.image.handler import ImageFileHandler
from mfr.docx.handler import DocxFileHandler
from mfr.rst.handler import RstFileHandler
from mfr.code.handler import CodeFileHandler
from mfr.pdf.handler import PdfFileHandler


# register module imports
# mfr.register_filehandler('image', ImageFileHandler)
mfr.register_filehandler('docx', DocxFileHandler)
mfr.register_filehandler('rst', RstFileHandler)
mfr.register_filehandler('code', CodeFileHandler)
mfr.register_filehandler('pdf', PdfFileHandler)

app = Flask(__name__, static_folder='files')


# Module static files should live in renderer/<module/static
@app.route('/render/static/<module>/<path:file_path>')
def send_module_file(module, file_path):
    file_path, file_name = os.path.split(file_path)
    module_static_dir = os.path.join('..', 'mfr', module, 'static', file_path)
    return send_from_directory(module_static_dir, file_name)

@app.route('/')
def index():
    html = ''
    for file_name in os.listdir('files'):
        fp = open(os.path.join('files', file_name))
        handler = mfr.detect(fp)
        safe_name = quote(file_name)
        if handler:
            html += '<a href="/render/{safe_name}">{file_name}</a>'.format(
                safe_name=safe_name, file_name=file_name)
            exporters = mfr.get_file_exporters(handler)
            if exporters:
                html += "<span style='margin:20px;'>export to:</span>"
                for exporter in exporters:
                    html += '<a href="/export/{exporter}/{file_name}" style="margin:10px;"> {exporter} </a>'.format(exporter=exporter, file_name=file_name)
        else:
            html += '<span>' + file_name + "</span>"
        html += "</br>"
    return html


@app.route('/render/<file_name>')
def render(file_name):
    fp = open(os.path.join('files', file_name))

    handler = mfr.detect(fp)


    # exp = export(fp, handler, exporter="png")
    # send_file(
    #     StringIO(exp),
    #     as_attachment=True,
    #     attachment_filename=export_name,
    #     )

    if handler:
        try:
            return mfr.render(fp, handler)
        except Exception as err:
            return err.message
    return file_name

@app.route('/export/<exporter>/<file_name>')
def export(exporter, file_name):
    print exporter
    print file_name
    fp = open(os.path.join('files', file_name))
    handler = mfr.detect(fp)
    exp = mfr.export(fp, handler, exporter="png")
    short_name, _ = os.path.splitext(file_name)
    export_name = short_name + '.' + exporter
    return send_file(
            StringIO(exp),
            as_attachment=True,
            attachment_filename=export_name,
            )



if __name__ == '__main__':
    app.run(debug=True, port=5001)