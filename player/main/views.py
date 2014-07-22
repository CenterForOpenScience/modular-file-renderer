# -*- coding: utf-8 -*-
"""
    main.views
    ~~~~~~~~~~

    Views for the main module

    :author: Elijah Hamovitz
"""
from __future__ import unicode_literals

import os

import mfr
from flask import render_template, Blueprint, current_app

mod = Blueprint('main', __name__)


@mod.route('/', methods=['GET'])
def index():
    files = []

    for f in os.listdir(current_app.config['FILES_DIR']):

        # ignore dotfiles
        if f.startswith('.'):
            continue

        fp = open(os.path.join(current_app.config['FILES_DIR'], f))
        # List of all modules for this file type
        handlers = mfr.detect(fp, many=True)

        renderer_handlers = [mfr.get_namespace(handler) for handler in handlers if handler.renderers]
        exporter_handlers = [handler for handler in handlers if handler.exporters]

        # Generate a list of modules and their file extensions
        export_options = []
        for handler in exporter_handlers:
            available_file_extensions = mfr.get_file_exporters(handler)
            for export_file_type in available_file_extensions:
                export_options.append((export_file_type, mfr.get_namespace(handler)))

        files.append((f, renderer_handlers, export_options))

    return render_template('main/index.html', files=files)
