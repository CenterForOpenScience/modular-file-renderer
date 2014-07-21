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
        # List of all renderer modules for this file type
        renderers = mfr.detect(fp, type="RENDERERS", many=True)

        # List of all exporter modules for this file type
        exporter_modules = mfr.detect(fp, type="EXPORTERS", many=True)

        # Generate a list of modules and their file extensions
        export_options = []
        for module in exporter_modules:
            available_file_extensions = mfr.get_file_exporters(module)
            for export_file_type in available_file_extensions:
                export_options.append((export_file_type, module.name))

        files.append((f, renderers, export_options))

    return render_template('main/index.html', files=files)
