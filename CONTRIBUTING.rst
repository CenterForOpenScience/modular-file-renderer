***********************
Contributing guidelines
***********************

In General
==========

- `PEP 8`_, when sensible.
- Test ruthlessly. Write docs for new features.
- Even more important than Test-Driven Development--*Human-Driven Development*.

.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/


Setting up for development
==========================

Clone the repo: ::

    $ git clone https://github.com/CenterForOpenScience/modular-file-renderer.git
    $ cd modular-file-renderer

Install the development dependencies. ::

    $ pip install -r dev-requirements.txt

.. note::

    It is recommended that you use a `virtualenv`_ during development.


Lastly, install mfr in development mode. ::

    $ python setup.py develop

.. _virtualenv: http://www.virtualenv.org/en/latest/


Writing A File Format Package
=============================

There are two main pieces of a file format package are

- Your custom rendering and/or exporting code
- Your :class:`FileHandler <mfr.core.FileHandler>`


Rendering/Exporting Code
------------------------

Renderes are simply callables (functions or methods) that take a file as their first argument and return a string of the rendered HTML.

Here is a very simple example of function that takes a filepointer and outputs an HTML image tag from it.

.. code-block:: python

    def render_img_tag(filepointer):
        filename = filepointer.name
        return '<img src="{filename}" />'.format(filename=filename)


You can also write renderers as methods.

TODO: Show examples of renderers as functions, instance methods, class or static methods, etc.

The FileHandler
---------------

A file handler is responsible for using your custom rendering and exporting code to actually render and export a file. When you call :func:`mfr.detect <mfr.detect>`, you receive a :class:`FileHandler <mfr.core.FileHandler>` class.

Your FileHandler **must** define a ``detect`` method which, given a file object, returns whether or not it can handle the file.

.. code-block:: python

    from mfr import FileHandler, get_file_extension

    # Your custom code
    from mfr.image.render import render_img_tag
    from mfr.image.export import ImageExporter


    class ImageFileHandler(FileHandler):
        renderers = {
            # like functions
            'html': render_img_tag,
        }

        exporters = {
            # Or instance methods
            'png': ImageExporter().export_png,
            'jpg': ImageExporter().export_jpg,
            # ...
        }

        def detect(self, fp):
            return get_file_extension(fp.name) in ['.jpg', '.png', ]  # and so on



Organization
------------

Each package has its own directory. At a minimum, your package should include:

- ``handler.py``: Where your :class:`FileHandler <mfr.core.FileHandler>`` subclass will live.
- ``render-requirements.txt``: External dependencies for rendering functionality.
- ``export-requirements.txt``: External dependencies for export functionality.

Apart from those files, you  are free to organize your rendering and export code however you want.

A typical directory structure might look like this.

::

    myformat
    ├── __init__.py
    ├── export-requirements.txt
    ├── export.py
    ├── handler.py
    ├── render-requirements.txt
    ├── render.py
    ├── static
    └── test_myformat.py

.. note::

    You may decide to make subdirectories for rendering and exporting code if  single files start to become very large.


Running tests
=============

To run all tests (requires pytest) ::

    $ invoke test

You can also use pytest directly. ::

    $ py.test

Writing tests
=============

TODO

Using the previewer
===================

The mfr comes with a Flask app for previewing rendered files.

To run the app, run: ::

    $ invoke previewer

Then browse to ``localhost:5000`` in your browser.


Documentation
=============

Contributions to the documentation are welcome. Documentation is written in `reStructured Text`_ (rST). A quick rST reference can be found `here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_. Builds are powered by Sphinx_.

To build docs: ::

    $ invoke docs -b

The ``-b`` (for "browse") automatically opens up the docs in your browser after building.

.. _Sphinx: http://sphinx.pocoo.org/

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
