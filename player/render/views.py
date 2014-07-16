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
@mod.route('/render/<renderer_name>/<filename>', methods=['GET'])
def render(filename, renderer_name=None):
    try:
        fp = open(os.path.join(current_app.config['FILES_DIR'], filename))
    except IOError as err:
        flash(err, 'error')
        abort(501)

    renderer = None
    if renderer_name is None:
        renderer = mfr.detect(fp, many=False)  # return the first valid filehandler
    else:
        renderers = get_registry(type="RENDERERS")

        for available_renderer in renderers:
            if available_renderer.name == renderer_name:
                renderer = available_renderer()
        if renderer is None:
            raise IOError('Specified renderer cannot be used with that file.')

    try:
        src = url_for('render.serve_file', filename=filename)
        return mfr.render(fp, handler=renderer, src=src)
    except Exception as err:
        flash(err, 'error')
        abort(501)

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


#TODO(asmacdo) whoa. export type is hardcoded to png. all this does is change the extension...
@mod.route('/export/<export_file_type>/<filename>')
@mod.route('/export/<handler_name>/<export_file_type>/<filename>', methods=['GET'])
def export(export_file_type, filename, handler_name=None):
    try:
        fp = open(os.path.join(current_app.config['FILES_DIR'], filename))
    except IOError as err:
        flash(err, 'error')
        abort(404)

    # If handler name is not specified, choose the first that will work
    if handler_name is None:
        handler = mfr.detect(fp)
        exp = mfr.export(fp, handler, exporter=export_file_type)
        short_name, _ = os.path.splitext(filename)
        export_name = short_name + '.' + export_file_type
        return send_file(
            StringIO(exp),
            as_attachment=True,
            attachment_filename=export_name,
        )

    else:
        handlers = get_registry(type="EXPORTERS")
        for handler in handlers:
            if handler.name == handler_name:
                exp = mfr.export(fp, handler=handler(), exporter=export_file_type)
                short_name, _ = os.path.splitext(filename)
                export_name = short_name + '.' + export_file_type
                return send_file(
                    StringIO(exp),
                    as_attachment=True,
                    attachment_filename=export_name,
                )

    return "Error, no valid handlers called ", handler_name