***
mfr
***

**mfr** (short for "Modular File Renderer") is a Python package for rendering files to HTML.


Usage
=====

Detect a file's type and render it to HTML.

.. code-block:: python

    import mfr
    import mfr_image

    # Enable the ImageModule
    mfr.register_filehandler(mfr_image.Handler)

    filepointer = open('hello.jpg')
    # Get available FileHandlers for the detected filetype
    handlers = mfr.detect(filepointer)

    # Render the file to html
    handlers[0].render(filepointer, alt="Hello world")
    # => '<img src="hello.jpg" alt="Hello world" />'


Or do it all in one step.

.. code-block:: python

    rendered = mfr.render(open('myimage.png'))
    # => '<img src="myimage.png" alt="" />'


Some renderers may require static assets (JS and CSS files). To collect all the necessary static assets into a single directory, use ``mfr.collect_static()``.

.. code-block:: python

    import mfr
    import mfr_code_pygments

    # The code module requires pygments CSS files
    mfr.register_filehandler(mfr_code_pygments.Handler)

    # Copy all necessary static files (e.g. style.css)
    mfr.collect_static(dest='/path/to/app/static')


You will now be able to include the static assets in your HTML:

.. code-block:: html

    <link rel="stylesheet" href="/path/to/app/static/mfr_code_pygments/css/style.css">

You can configure mfr via the ``mfr.config`` object.

.. code-block:: python

    import mfr
    import mfr_image
    import mfr_code_pygments

    mfr.config({
        # Static assets will be collected here
        'STATIC_FOLDER': '/path/to/static/folder',
        # Your app's base URL for static files
        'STATIC_URL': '/static',
        # Another way to register handlers
        'HANDLERS': [mfr_image.Handler, mfr_code_pygments.Handler]
    })

    mfr.config['STATIC_FOLDER']  #=> '/path/to/static/folder'
    mfr.collect_static()  # copies static files to '/path/to/static/folder'

The config object has the same the same API as `Flask's config module`_. The following example is equivalent to above.

.. code-block:: python

    class MFRConfig:
        STATIC_FOLDER = '/path/to/static/folder'
        STATIC_URL = '/static'
        HANDLERS = [mfr_image.Handler, mfr_code_pygments.Handler]

    mfr.config.from_object(MFRConfig)
    mfr.config['STATIC_FOLDER']  #=> '/path/to/static/folder'
    mfr.collect_static()



.. _Flask's config module: http://flask.pocoo.org/docs/api/#configuration

Example Usage with Flask
========================

Below is an example `Flask`_ application that uses mfr.

.. _Flask: http://flask.pocoo.org

.. code-block:: python

    from flask import Flask, url_for, send_from_directory

    import mfr
    import mfr_image

    app = Flask(__name__)

    @app.route('/view/<filename>')
    def view_file(filename):
        with open(os.path.join('/path/to/uploads/', filename)) as fp:
            # Get first available handler for the file
            handler = mfr.detect(fp)[0]
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


    def main():
        # Configure MFR with correct static URL and folder
        mfr.config({
            'STATIC_URL': app.static_url_path,
            'STATIC_FOLDER': app.static_folder,
            # Register handlers through config
            'HANDLERS': [mfr_image.Handler]
        })
        app.run(debug=True)

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
