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

        handler_dict = {}
        for handler in handlers:
            exporters = mfr.get_file_exporters(handler)
            handler_dict[handler] = exporters

        files.append((f, handler_dict))

    return render_template('main/index.html', files=files)
