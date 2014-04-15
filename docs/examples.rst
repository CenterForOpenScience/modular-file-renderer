.. _examples:

********
Examples
********

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
