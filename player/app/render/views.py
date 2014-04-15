# -*- coding: utf-8 -*-
"""
    main.views
    ~~~~~~~~~~~

    Views for the main module

    :author: Elijah Hamovitz
    :copyright: (c) 2014 by Elijah Hamovitz.
"""
from __future__ import unicode_literals

import os
import mfr

from cStringIO import StringIO

from flask import Blueprint, flash, url_for, current_app, send_file, send_from_directory, abort

mod = Blueprint('render', __name__)


@mod.route('/render/<filename>', methods=['GET'])
def render(filename):
    fp = open(os.path.join(current_app.config['FILES_DIR'], filename))
    handler = mfr.detect(fp, many=False)  # return the first valid filehandler
    if handler:
        try:
            src = url_for('render.serve_file', filename=filename)
            return mfr.render(fp, handler=handler, src=src)
        except Exception as err:
            flash(err.message, 'error')
            abort(404)
    flash('Do not know how to render file {filename}'.format(filename=filename), 'error')
    abort(404)

@mod.route('/files/<filename>')
def serve_file(filename):
    return send_from_directory(current_app.config['FILES_DIR'], filename)

@mod.route('/render/static/<module>/<path:file_path>')
def send_module_file(module, file_path):
    file_path, filename = os.path.split(file_path)
    module_static_dir = os.path.join('..', 'mfr', module, 'static', file_path)
    return send_from_directory(module_static_dir, filename)

@mod.route('/export/<exporter>/<filename>')
def export(exporter, filename):
    fp = open(os.path.join(current_app.config['FILES_DIR'], filename))
    handler = mfr.detect(fp)
    exp = mfr.export(fp, handler, exporter="png")
    short_name, _ = os.path.splitext(filename)
    export_name = short_name + '.' + exporter
    return send_file(
        StringIO(exp),
        as_attachment=True,
        attachment_filename=export_name,
    )
