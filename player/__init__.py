# -*- coding: utf-8 -*-
"""
    MFR Player
    ~~~~~~~~~~

    Simple barebones flask project to bootstrap the MFR on top of a
    locally-hosted directory of files.

    :author: Elijah Hamovitz
"""
from flask import Flask, render_template

import mfr
import mfr_image
import mfr_docx
import mfr_rst
import mfr_md
import mfr_code_pygments

# TODO this is rather gross; the MFR Code Pygments module really neesd a
# much better configuration system
from mfr_code_pygments.configuration import config as mfr_code_config
mfr_code_config['PYGMENTS_THEME'] = 'manni'


def create_app(**kwargs):
    """Create and return an Flask app instance"""

    # create app; load config

    app = Flask(__name__)
    app.config.from_object('player.config')
    app.config.update(**kwargs)

    # Configure MFR

    class MFRConfig:
        # Base URL for static files
        STATIC_URL = app.static_url_path
        # Where to save static files
        STATIC_FOLDER = app.static_folder
        # Allow renderers to include static asset imports
        INCLUDE_STATIC = True

        # Available file handlers
        HANDLERS = [mfr_image.Handler,
                    mfr_docx.Handler,
                    mfr_rst.Handler,
                    mfr_md.Handler,
                    mfr_code_pygments.Handler]
    mfr.config.from_object(MFRConfig)
    mfr.collect_static()

    # Set up error handlers

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def generic_server_error(error):
        return render_template('500.html'), 500

    @app.errorhandler(501)
    def not_implemented_error(error):
        return render_template('501.html'), 501

    # register blueprints

    from main.views import mod as main_module
    app.register_blueprint(main_module)

    from render.views import mod as render_module
    app.register_blueprint(render_module)

    return app
