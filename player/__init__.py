# -*- coding: utf-8 -*-
"""
    MFR Player
    ~~~~~~~~~~

    Simple barebones flask project to bootstrap the MFR on top of a
    locally-hosted directory of files.

    :author: Elijah Hamovitz
"""
import os
from flask import Flask, render_template

import mfr

HERE = os.path.abspath(os.path.dirname(__file__))

def create_app(**kwargs):
    """Create and return a Flask app instance"""

    # create app; load config
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(HERE, 'app_config.py'))
    app.config.update(**kwargs)

    # Configure MFR
    mfr.config.from_pyfile(os.path.join(HERE, 'mfr_config.py'))
    # Local overrides
    mfr.config.from_pyfile(os.path.join(HERE, 'mfr_config_local.py'), silent=True)
    # update static url and folder
    mfr.config.update({
        # Base URL for static files
        'STATIC_URL': os.path.join(app.static_url_path, 'mfr'),
        # Where to save static files
        'STATIC_FOLDER': os.path.join(app.static_folder, 'mfr'),
    })
    app.logger.debug('Config: {0}'.format(mfr.config))
    app.logger.debug('Registered handlers: {0}'.format(mfr.config['HANDLERS']))
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

    from .main.views import mod as main_module
    app.register_blueprint(main_module)

    from .render.views import mod as render_module
    app.register_blueprint(render_module)

    return app
