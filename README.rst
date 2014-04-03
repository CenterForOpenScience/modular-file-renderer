***
mfr
***

**mfr** (short for "Modular File Renderer") is a Python package for rendering files to HTML.


Detect a file's type and render it to HTML.

.. code-block:: python

    import mfr

    filepointer = open('hello.jpg')
    # Get a FileHandler for the detected filetype
    handler = mfr.detect(filepointer)

    # Render the file to html
    handler.render(filepointer, alt="Hello world")
    # => '<img src="hello.jpg" alt="Hello world" />'


Or do it all in one step.

.. code-block::

    rendered = mfr.render(open('myimage.png'))
    # => '<img src="myimage.png" alt="" />'


Requirements
============

- Python >= 2.6 or >= 3.3


Installing Extra Dependencies
=============================

TODO




License
=======

TODO
