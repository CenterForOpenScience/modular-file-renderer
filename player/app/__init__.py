# -*- coding: utf-8 -*-
"""
    MFR Player
    ~~~~~~~~~~

    Simple barebones flask project to bootstrap the MFR on top of a
    locally-hosted directory of files.

    :author: Elijah Hamovitz
"""
from flask import Flask, render_template

# TODO the mfr import and configuration system could use a whole ton of
# work. Highest priority is putting that pygments theme config option
# into the main config object with everything else. Second priority is
# coming up with a much more dynamic way to configure the MFR based on
# this app
import mfr
import mfr_image
import mfr_docx
import mfr_rst
import mfr_md
import mfr_code_pygments
from mfr_code_pygments.configuration import config as mfr_code_config
mfr_code_config['PYGMENTS_THEME'] = 'manni'


def create_app(config_overrides={}):
    """Create and return an Flask app instance"""
    # create app; load config
    app = Flask(__name__)
    app.config.from_object('config')
    app.config.update(**config_overrides)

    @app.before_request
    def before_request():
        # TODO as referenced above, this needs to be fixed
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
    from app.main.views import mod as main_module
    app.register_blueprint(main_module)

    from app.render.views import mod as render_module
    app.register_blueprint(render_module)

    return app
