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
        handlers = mfr.detect(fp, many=True)

        exporter_modules = mfr.detect(fp, handlers=mfr.get_exporters(), many=True)
        export_options = []
        for module in exporter_modules:
            exporters = mfr.get_file_exporters(module)
            for exporter in exporters:
                export_options.append((exporter, module.name))

        files.append((f, handlers, export_options))

    return render_template('main/index.html', files=files)
