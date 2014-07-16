# -*- coding: utf-8 -*-
"""
    render.views
    ~~~~~~~~~~~~

    Views for the render module

    :author: Elijah Hamovitz
"""
from __future__ import unicode_literals

import os
import mfr

from cStringIO import StringIO

from flask import Blueprint, flash, url_for, current_app, send_file, \
    send_from_directory, abort

from mfr.core import get_registry

mod = Blueprint('render', __name__)


@mod.route('/render/<filename>', methods=['GET'])
def render(filename):
    try:
        fp = open(os.path.join(current_app.config['FILES_DIR'], filename))
    except IOError as err:
        flash(err, 'error')
        abort(404)

    handler = mfr.detect(fp, many=False)  # return the first valid filehandler
    if handler:
        try:
            src = url_for('render.serve_file', filename=filename)
            return mfr.render(fp, handler=handler, src=src)
        except Exception as err:
            flash(err, 'error')
            abort(404)

    abort(501)

@mod.route('/render_with/<handler_name>/<filename>', methods=['GET'])
def render_with(filename, handler_name):
    try:
        fp = open(os.path.join(current_app.config['FILES_DIR'], filename))
    except IOError as err:
        flash(err, 'error')
        abort(404)

    handlers = get_registry()

    for handler in handlers:
        if handler.name == handler_name:
            try:
                src = url_for('render.serve_file', filename=filename)
                return mfr.render(fp, handler=handler(), src=src)
            except Exception as err:
                flash(err, 'error')
                abort(404)
    return "no valid handlers"


@mod.route('/files/<filename>')
def serve_file(filename):
    try:
        return send_from_directory(current_app.config['FILES_DIR'], filename)
    except IOError as err:
        flash(err, 'error')
        abort(404)


@mod.route('/render/static/<module>/<path:file_path>')
def send_module_file(module, file_path):
    file_path, filename = os.path.split(file_path)
    module_static_dir = os.path.join('..', 'mfr', module, 'static', file_path)
    try:
        return send_from_directory(module_static_dir, filename)
    except IOError as err:
        flash(err, 'error')
        abort(404)


@mod.route('/export/<exporter>/<filename>')
@mod.route('/export_with/<handler_name>/<exporter>/<filename>', methods=['GET'])
def export(exporter, filename, handler_name=None):
    try:
        fp = open(os.path.join(current_app.config['FILES_DIR'], filename))
    except IOError as err:
        flash(err, 'error')
        abort(404)

    # If handler name is not specified, choose the first that will work
    if handler_name is None:
        handler = mfr.detect(fp)
        exp = mfr.export(fp, handler, exporter="png")
        short_name, _ = os.path.splitext(filename)
        export_name = short_name + '.' + exporter
        return send_file(
            StringIO(exp),
            as_attachment=True,
            attachment_filename=export_name,
        )

    else:
        handlers = get_registry(type="EXPORTERS")
        for handler in handlers:
            if handler.name == handler_name:
                exp = mfr.export(fp, handler=handler(), exporter="png")
                short_name, _ = os.path.splitext(filename)
                export_name = short_name + '.' + exporter
                return send_file(
                    StringIO(exp),
                    as_attachment=True,
                    attachment_filename=export_name,
                )

    return "Error, no valid handlers called ", handler_name