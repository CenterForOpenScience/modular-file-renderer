***********************
Contributing guidelines
***********************

In general
==========

- `PEP 8`_, when sensible.
- Test ruthlessly. Write docs for new features.
- Even more important than Test-Driven Development--*Human-Driven Development*.
- Please update AUTHORS.rst when you contribute.

.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/

In particular
=============


Setting up for development
--------------------------

Clone the repo: ::

    $ git clone https://github.com/CenterForOpenScience/modular-file-renderer.git
    $ cd modular-file-renderer

Install the development dependencies.

.. note::

    It is recommended that you use a `virtualenv`_ during development.

.. _virtualenv: http://www.virtualenv.org/en/latest/

::

    $ pip install -r dev-requirements.txt




Lastly, install mfr in development mode. ::

    $ python setup.py develop


Running tests
-------------


To run all tests (requires pytest) ::

    $ invoke test

You can also use pytest directly. ::

    $ py.test

Writing tests
-------------

Unit tests should be written for all rendering, exporting, and detection code.

Tests can be written as functions, like so:

.. code-block:: python

    # in test_myformat.py

    from mfr_something import render

    def test_render_html():
        with open('testfile.mp4') as fp:
            assert render.render_html(fp) == '<p>rendered testfile.mp4</p>'

There are a few `pytest fixtures`_ to help you mock files. You can use them by simply including them as parameters to your test functions. For example, the ``fakefile`` fixture is a fake file-like object whose name and content you can set to any value.

The above test can be rewritten like so:

.. code-block:: python

    # in test_myformat.py

    from mfr_something import render

    def test_render_html(fakefile):
        assert render.render_html(fakefile) == '<p>rendered testfile.mp4</p>'

.. _pytest fixtures: https://pytest.org/latest/fixture.html

Using the player
----------------

The mfr comes with a Flask app for previewing rendered files. Copy the files you want to render to the ``player/files`` directory then run the app from the ``player`` directory with ::

    $ invoke player

Then browse to ``localhost:5000`` in your browser.

Configuring the player
++++++++++++++++++++++

You will likely want to add additional filehandler modules to the player. The first time you run ``invoke player``, a file is created at ``player/mfr_config_local.py``. You can add additional handlers to the ``HANDLERS`` list and add any additional configuration here.

.. code-block:: python

    # in player/mfr_config_local.py

    import mfr_image
    import mfr_code_pygments

    # Add additional handlers here
    HANDLERS = [
        mfr_image.Handler,
        mfr_code_pygments.Handler,
    ]



Writing A File Format Package
-----------------------------

There are two main pieces of a file format package are

- Your custom rendering and/or exporting code
- Your :class:`FileHandler <mfr.core.FileHandler>`


Rendering/Exporting Code
++++++++++++++++++++++++

Renderers are simply callables (functions or methods) that take a file as their first argument and return a :class:`RenderResult <mfr.core.RenderResult>` which contains content(a string of the rendered HTML) and assets (a dictionary that points to lists of javascript or css sources).

Here is a very simple example of function that takes a filepointer and outputs a render result with an HTML image tag.

.. code-block:: python
    from mfr import RenderResult

    def render_img_tag(filepointer):
        filename = filepointer.name
        content = '<img src="{filename}" />'.format(filename=filename)
        return RenderResult(content)

You can also write renderers as methods.

.. code-block:: python

    # in mfr_video/render.py

    class VideoRenderer(object):

        def render_html5_tag(self, fp):
            content = '<video src="{filename}"></video>'.format(filename=fp.name)
            return RenderResult(content)

        def render_flash(self, fp):
            # ...
            pass


The FileHandler
+++++++++++++++

A file handler is responsible for using your custom rendering and exporting code to actually render and export a file. When you call :func:`mfr.detect <mfr.detect>`, you receive a list of :class:`FileHandler <mfr.core.FileHandler>` classes.

Your FileHandler **must** define a ``detect`` method which, given a file object, returns whether or not it can handle the file.

**Your FileHandler class should be named Handler and should be defined in your `mfr_format/__init__.py` file.**

.. code-block:: python

    # in mfr_image/__init__.py

    from mfr import FileHandler, get_file_extension

    # Your custom code
    from mfr_image.render import render_img_tag
    from mfr_image.export import ImageExporter


    class Handler(FileHandler):
        renderers = {
            'html': render_img_tag,
        }

        exporters = {
            'png': ImageExporter().export_png,
            'jpg': ImageExporter().export_jpg,
            # ...
        }

        def detect(self, fp):
            return get_file_extension(fp.name) in ['.jpg', '.png', ]  # and so on



Organization
++++++++++++

Each package has its own directory. At a minimum, your package should include:

- ``__init__.py``: Where your :class:`FileHandler <mfr.core.FileHandler>`` subclass will live.
- ``render-requirements.txt``: External dependencies for rendering functionality.
- ``export-requirements.txt``: External dependencies for export functionality.

Apart from those files, you  are free to organize your rendering and export code however you want.

A typical directory structure might look like this:

::

	mfr
	└──mfr-something
		├── export-requirements.txt
		├── render-requirements.txt
		├── __init__.py
		├── render.py
		├── export.py
		├── static
		│   ├── js
		│   └── css
		├── tests
		│   ├── __init__.py
		│   └── test_something.py
		├── templates
		│   └── something.html
		├── libs
		│   ├── __init__.py
		│   └── something_tools.py
		├── setup.py
		├── README.rst
		└── configuration.py

where "something" is a file format, e.g. "mfr_image", "mfr_movie".

.. note::

    You may decide to make subdirectories for rendering and exporting code if single files start to become very large.


Use a template
++++++++++++++

The fastest way to get started on a module is to use `cookiecutter template`_ for mfr modules. This will create the directory structure above.

::

    $ pip install cookiecutter
    $ cookiecutter https://github.com/CenterForOpenScience/cookiecutter-mfr.git

.. _cookiecutter template: https://github.com/CenterForOpenScience/cookiecutter-mfr



Documentation
-------------

Contributions to the documentation are welcome. Documentation is written in `reStructured Text`_ (rST). A quick rST reference can be found `here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_. Builds are powered by Sphinx_.

To build docs: ::

    $ invoke docs -b

The ``-b`` (for "browse") automatically opens up the docs in your browser after building.

.. _Sphinx: http://sphinx.pocoo.org/

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
