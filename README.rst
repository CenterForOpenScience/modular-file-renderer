***
mfr
***

**mfr** (short for "Modular File Renderer") is a Python package for rendering files to HTML.


Usage
=====

Detect a file's type and render it to HTML.

.. code-block:: python

    import mfr
    from mfr.image.handler import ImageFileHandler

    # Enable the ImageModule
    mfr.register_filehandler('image', ImageFileHandler)

    filepointer = open('hello.jpg')
    # Get a FileHandler for the detected filetype
    handler = mfr.detect(filepointer)

    # Render the file to html
    handler.render(filepointer, alt="Hello world")
    # => '<img src="hello.jpg" alt="Hello world" />'


Or do it all in one step.

.. code-block:: python

    rendered = mfr.render(open('myimage.png'))
    # => '<img src="myimage.png" alt="" />'


Some renderers may require static assets (JS and CSS files). To collect all the necessary static assets into a single directory, use ``mfr.collect_static()``.

.. code-block:: python

    import mfr
    from mfr.code.handler import CodeFileHandler

    # The code module requires pygments CSS files
    mfr.register_filehandler('code', CodeFileHandler)

    # Copy all necessary static files (e.g. style.css)
    mfr.collect_static(dest='/path/to/app/static')


You will now be able to include the static assets in your HTML:

.. code-block:: html

    <link rel="stylesheet" href="/path/to/app/static/code/css/style.css">

You can configure mfr via the ``mfr.config`` object, which has the same API as `Flask's config module`_.

.. _Flask's config module: http://flask.pocoo.org/docs/api/#configuration

.. code-block:: python

    import mfr

    class MFRConfig:
        # Static assets will be collected here
        STATIC_FOLDER = '/path/to/static/folder'
        # Your app's base URL for static files
        STATIC_URL = '/static'

    mfr.config.from_object(MFRConfig)

    mfr.collect_static()  # copies static files to '/path/to/static/folder'



Example Flask Usage
===================

Below is an example `Flask`_ application that uses mfr.

.. _Flask: http://flask.pocoo.org

.. code-block:: python

    from flask import Flask, url_for, send_from_directory
    import mfr

    app = Flask(__name__)

    class MFRConfig:
        STATIC_URL = app.static_url_path
        STATIC_FOLDER = app.static_folder

    class AppConfig:
        UPLOADS_FOLDER = '/path/to/uploads/'

    @app.route('/view/<filename>')
    def view_file(filename):
        fp = open(os.path.join(app.config['UPLOADS_FOLDER'], filename))
        # Get a handler for the file
        handler = mfr.detect(fp)
        if handler:
            # some renderers, e.g. the image renderer, require a src argument
            src = url_for('serve_file', filename=filename)
            rendered_html = handler.render(fp, src=src)
            return render_template('view_file.html', rendered=rendered_html)
        else:
            return 'Cannot render {filename}.'.format(filename=filename)

    @app.route('/files/<filename>')
    def serve_file(filename):
        return send_from_directory(app.config['FILES_DIR'], filename)

    def main(*args, **kwargs):
        mfr.config.from_object(MFRConfig)
        app.config.from_object(AppConfig)
        mfr.collect_static()
        app.run(*args, **kwargs)

    if __name__ == '__main__':
        main()


Requirements
============

- Python >= 2.6 or >= 3.3


Installing Extra Dependencies
=============================

TODO


License
=======

TODO
