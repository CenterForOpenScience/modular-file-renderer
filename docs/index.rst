.. mfr documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

mfr: HTML file renderer for Python
==================================

Release v\ |version|. (:ref:`Installation <install>`)

**mfr** (short for "modular file renderer") is a Python package for rendering files to HTML.

.. code-block:: python

    import mfr
    import mfr_image

    # Enable the ImageModule
    mfr.register_filehandler(mfr_image.Handler)

    with open('hello.jpg') as filepointer:
       mfr.render(filepointer, alt="Hello world")
       # => '<img src="hello.jpg" alt="Hello world" />'


Ready to dive in?
-----------------

Go on to the :ref:`Quickstart tutorial <quickstart>` or check out some :ref:`examples <examples>`.


Guide
-----

.. toctree::
   :maxdepth: 1

   license
   install
   quickstart
   examples
   api_reference

Project info
------------

.. toctree::
   :maxdepth: 1

   contributing
   authors
   changelog
