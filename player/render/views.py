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
    """Make a file viewable in HTML

    :param filename: file to be rendered
    :param renderer_name: optional name of the specific renderer module
    :return: html representation of the file
    """

    try:
        fp = open(os.path.join(current_app.config['FILES_DIR'], filename))

    except IOError as err:
        print 'hello'
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
        rendered_result = mfr.render(fp, handler=renderer, src=src)
        print 'HELLO'
        return '\n'.join([rendered_result.assets.get("css", '<style></style>'), rendered_result.content_html])

    except Exception as err:
        flash(err, 'error')
        abort(501)

@mod.route('/files/<filename>')
def serve_file(filename):
    """Serve the file (not rendered)

    :param filename: file to be shown
    :return: file
    """

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


@mod.route('/export/<export_file_type>/<filename>')
@mod.route('/export/<exporter_name>/<export_file_type>/<filename>', methods=['GET'])
def export(export_file_type, filename, exporter_name=None):
    """ Convert a file to another type and download that file.

    :param export_file_type: the type to export a file as
    :param filename: file to be exported
    :param exporter_name: optional name of the specific exporter module
    """

    try:
        fp = open(os.path.join(current_app.config['FILES_DIR'], filename))
    except IOError as err:
        flash(err, 'error')
        abort(404)

    # If handler name is not specified, choose the first that will work
    if exporter_name is None:
        exporter = mfr.detect(fp, type="EXPORTERS", many=False)
        exp = mfr.export(fp, exporter, exporter=export_file_type)

    else:
        handlers = get_registry(type="EXPORTERS")
        for handler in handlers:
            if handler.name == exporter_name:
                exp = mfr.export(fp, handler=handler(), exporter=export_file_type)

    if not exp:
        raise NameError("A matching exporter not found")

    short_name, _ = os.path.splitext(filename)
    export_name = short_name + '.' + export_file_type

    return send_file(
        StringIO(exp),
        as_attachment=True,
        attachment_filename=export_name,
    )