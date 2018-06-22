.. _quickstart:

**********
Quickstart
**********


.. code-block:: python

    with open('mycode.img') as filepointer:
        handler = mfr.detect(filepointer)  # returns a handler object
        if handler:
            render_result = handler.render(filepointer)
        else:
            content = '<p>Cannot render file.</p>'
            render_result = mfr.RenderResult(content=content)

You can also use :func:`mfr.render <mfr.core.render>` to perform detection and rendering simultaneously. If no valid handler for a file is available, a ``ValueError`` is raised.

This example is equivalent to above.

.. code-block:: python

    with open('mycode.img') as filepointer:
        try:
            render_result = mfr.render(filepointer)
        except ValueError:  # No valid handler available
            render_result = mfr.RenderResult('<p>Cannot render file.</p>')


RenderResult objects contain the resultant html as content. Any javascript or css assets are contained in a dictionary. To display assets with jinja, simply iterate through the lists.

.. code-block:: none

    {% for stylesheet in render_result.assets.css %}
        <link rel="stylesheet" href={{ stylesheet }}/>
    {%  endfor %}

    {% for javascript in render_result.assets.js %}
        <script type="text/javascript" src={{ javascript }}/>
    {%  endfor %}

    {{ render_result.content|safe }}

Configuration
=============

In order to use mfr in a web application, you will need to configure mfr with certain facts about the application, e.g. the base URL from which static files are served and the folder where to store static assets.

Configuration is stored on a ``mfr.config``, which can be modified like a dictionary.

.. code-block:: python

    import mfr
    import mfr_code_pygments

    mfr.config['STATIC_URL'] = '/static'
    mfr.config['STATIC_FOLDER'] = '/path/to/app/static'

    # Filehandlers can be registered this way
    mfr.config['HANDLERS'] = [mfr_code_pygments.Handler]

.. note::

    The ``mfr.config`` shares the same API as `Flask's config <http://flask.pocoo.org/docs/config/>`_, so you can also load configuration values from files or Python objects.

    .. code-block:: python

        import mfr
        import mfr_code_pygments

        # Equivalent to above
        class MFRConfig:
            STATIC_URL = '/static'
            STATIC_FOLDER = '/path/to/app/static'
            HANDLERS = [mfr_code_pygments.Handler]

        mfr.config.from_object(MFRConfig)
        mfr.config['STATIC_URL']  # '/static'



Using Static Files
==================

Many renderers require static files (e.g. CSS and Javascript). To retrieve the static files for a file renderer, the object has a 'assets_url' that serves as the base path.


