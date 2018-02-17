***********************
Contributing guidelines
***********************

In general
==========

- `PEP 8`_, when sensible.
- Test ruthlessly. Write docs for new features.
- Even more important than Test-Driven Development--*Human-Driven Development*.
- If you add an extension to setup.py, add it to supportedextensions.md.
- Please update AUTHORS.rst when you contribute.

.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/

In particular
=============


Setting up for development
--------------------------

Clone the repo: ::

    $ git clone https://github.com/CenterForOpenScience/modular-file-renderer.git
    $ cd modular-file-renderer

Configure development environment and install the development dependencies.

.. note::

    It is recommended that you use a `virtualenv`_ with `virtualenvwrapper`_ during development. Python 3.5 or greater, `R`_, and `pspp`_ are required.

.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _virtualenvwrapper: https://pypi.python.org/pypi/virtualenvwrapper
.. _R: https://www.r-project.org/
.. _pspp: https://www.gnu.org/software/pspp/

.. code-block:: bash

    # For Mac OS X: Install the latest version of python3.5
    $ brew install python3
    $ brew install r pspp

    # Linux users, probably the same thing but with apt-get
    # If someone wants to update this guide, please do.

    $ pip install virtualenv
    $ pip install virtualenvwrapper
    $ mkvirtualenv --python=`which python3` mfr
    $ pip install setuptools==30.4.0
    $ pip install invoke==0.13.0


Lastly, install mfr in development mode. ::

    $ invoke install -d
    $ invoke server
   
Running tests
-------------


To run all tests (requires pytest) ::

    $ invoke test

You can also use pytest directly. ::

    $ py.test

Writing tests
-------------

Unit tests should be written for all rendering code.

Tests should be encapsulated within a class and written as functions, like so:

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


Manual Local Testing
--------------------

To make sure a new renderer is functioning properly, it's recommended that you try to render a file of that type locally. 

First, change the default provider to HTTP (in `/mfr/server/settings.py`), then update the provider domain in the ``ALLOWED_PROVIDER_DOMAINS`` whitelist (a space-separated string):

.. code-block:: python

    PROVIDER_NAME = config.get('PROVIDER_NAME', 'http')
    ALLOWED_PROVIDER_DOMAINS = config.get('ALLOWED_PROVIDER_DOMAINS', 'http://localhost:8000/')

Because the MFR is passed a url to render, you also need to be running an http server.

From a directory with a file you want to render:

.. code-block:: bash

    python -m SimpleHTTPServer 8000

Or for python 3

.. code-block:: bash

    python3 -m http.server 8000

With both the SimpleHTTPServer and the MFR server running, go to

.. code-block:: bash

	http://localhost:7778/render?url=http://localhost:8000/[filename].[ext]


Writing A File Format Package
-----------------------------

There are two main pieces of a file format package are

- Your custom rendering and/or exporting code
- Your :class:`FileHandler <mfr.core.FileHandler>`


Rendering Code
++++++++++++++++++++++++

Renderers are simply callables (functions or methods) that take a file as their first argument and return

Here is a very simple example of function that takes a filepointer and outputs a render result with an HTML image tag.

.. code-block:: python

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

A typical extension plugin directory structure might look like this:

::

	modular-file-renderer
	├── mfr
	│	├── __init__.py
	│	└── extensions
	│		├── __init__.py
	│		└── custom-plugin
	│			├── __init__.py
	│			├── render.py
	│			├── export.py
	│			├── settings.py
	│			├── static
	│			│	├── css
	│			│	└── js
	│			├── templates
	│			│	└── viewer.mako
	│			└── libs
	│				├── __init__.py
	│				└── tools.py
	├── tests
	│	├── __init__.py
	│	└── extensions
	│		├── __init__.py
	│		└── custom-plugin
	│			├── __init__.py
	│			└── test_custom_plugin.py
	├── setup.py
	├── README.md
	└── requirements.txt


Documentation
-------------

Contributions to the documentation are welcome. Documentation is written in `reStructured Text`_ (rST). A quick rST reference can be found `here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_. Builds are powered by Sphinx_.

To build docs: ::

    $ pip install -r doc-requirements.txt
    $ cd docs
    $ make html
    $ open _build/html/index.html

The ``-b`` (for "browse") automatically opens up the docs in your browser after building.

.. _Sphinx: http://sphinx.pocoo.org/

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
