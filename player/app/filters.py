# -*- coding: utf-8 -*-
"""
    filters
    ~~~~~~~

    Jinja filters for rendering the list of files

    :author: Elijah Hamovitz
"""
import os
import mfr
import jinja2
from urllib import quote

from flask import current_app

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
        fp = open(os.path.join(current_app.config['FILES_DIR'], filename))
        handler = mfr.detect(fp)
        if handler:
            html += '<a href="/render/{safe_name}">{filename} </a>'.format(
                safe_name=quote(filename),
                filename=filename)
            html += build_export_html(filename, handler)
        else:
            html += '<span>' + filename + "</span>"
    return jinja2.Markup(html)

