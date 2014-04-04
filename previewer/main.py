# -*- coding: utf-8 -*-
"""Flask app for previewing files.
"""


import os
import random

from urllib import quote
from flask import Flask, send_file
from cStringIO import StringIO
import mfr


# module imports
from mfr.image.handler import ImageFileHandler

# register module imports
mfr.register_filehandler('image', ImageFileHandler)

app = Flask(__name__, static_folder='files')


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