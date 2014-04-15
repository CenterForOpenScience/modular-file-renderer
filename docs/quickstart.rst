.. _quickstart:

**********
Quickstart
**********

Before we start rendering, we need to enable a file format's module. To do this, use :func:`mfr.register_filehandler <mfr.core.register_filehandler>`, passing in a :class:`FileHandler <mfr.core.FileHandler>`.

Let's use the ``mfr_code_pygments`` module as an example.

.. code-block:: python

    import mfr
    import mfr_code_pygments

    # Enable the ImageModule
    mfr.register_filehandler(mfr_code_pygments.Handler)


Then call :func:`mfr.detect <mfr.core.detect>` with a file object, which returns an instance of a handler that can handle the file, or ``None`` if no valid handler is registered.

.. code-block:: python

    with open('mycode.img') as filepointer:
        handler = mfr.detect(filepointer)  # returns a handler object
        if handler:
            html = handler.render(filepointer)
        else:
            html = '<p>Cannot render file.</p>'

You can also use :func:`mfr.render <mfr.core.render>` to perform detection and rendering simultaneously. If no valid handler for a file is available, a ``ValueError`` is raised.

This example is equivalient to above.

.. code-block:: python

    with open('mycode.img') as filepointer:
        try:
            html = mfr.render(filepointer)
        except ValueError:  # No valid handler available
            html = '<p>Cannot render file.</p>'

Configuration
=============

In order to use mfr in a web application, you will need to configure mfr with certain facts about the application, e.g. the base URL from which static files are served and the folder where to store static assets.

Configuration is stored on a ``mfr.config``, which can be modified like a dictionary.

.. code-block:: python

    import mfr

    mfr.config['STATIC_URL'] = '/static'
    mfr.config['STATIC_FOLDER'] = '/path/to/app/static'

    # Filehandlers can be registered this way
    mfr.config['HANDLERS'] = [mfr_code_pygments.Handler]

.. note::

    The ``mfr.config`` shares the same API as `Flask's config <http://flask.pocoo.org/docs/config/>`_, so you can also load configuration values from files or Python objects.

    .. code-block:: python

        import mfr

        # Equivalent to above
        class MFRConfig:
            STATIC_URL = '/static'
            STATIC_FOLDER = '/path/to/app/static'
            HANDLERS = [mfr_code_pygments.Handler]

        mfr.config.from_object(MFRConfig)
        mfr.config['STATIC_URL']  # '/static'



Using Static Files
==================

Many renderers require static files (e.g. CSS and Javascript). To retrieve the static files for a file handler, call its :func:`get_static <mfr.core.FileHandler.get_static>` method. This will return a dictionary which maps file extensions to a list of paths.

.. code-block:: python

    import mfr
    import mfr_code_pygments

    mfr.config['STATIC_URL'] = '/static'
    handler = mfr_code_pygments.Handler()
    handler.get_assets()['css']
    # ['/static/mfr_code_pygments/css/autumn.css',
    #  '/static/mfr_code_pygments/css/borland.css', ...

Copying Static Assets
---------------------

To copy all necessary static assets to your app's static folder, use :func:`collect_static <mfr.core.collect_static>`.

.. code-block:: python

    # Static assets will be copied here
    mfr.config['STATIC_FOLDER'] = '/app/static'
    mfr.collect_static()  # Copies static files to STATIC_FOLDER



