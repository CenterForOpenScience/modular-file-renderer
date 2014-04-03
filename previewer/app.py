# -*- coding: utf-8 -*-
"""Flask app for previewing files.
"""

from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return 'TODO'
