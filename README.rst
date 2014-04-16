***
mfr
***

**mfr** (short for "modular file renderer") is a Python package for rendering files to HTML.

.. code-block:: python

    import mfr
    import mfr_image

    # Enable the mfr_image module
    mfr.register_filehandler(mfr_image.Handler)

    with open('hello.jpg') as filepointer:
       mfr.render(filepointer, alt="Hello world")
       # => '<img src="hello.jpg" alt="Hello world" />'


Requirements
============

- Python >= 2.6 or >= 3.3


Available modules
=================

There are a number of 3rd-party modules available.

- `mfr-code-pygments <https://github.com/CenterForOpenScience/mfr-code-pygments>`_
- `mfr_md <https://github.com/TomBaxter/mfr_md>`_

Make your own, then submit a pull request to add it to this list!


Create your own module
======================

Interested in adding support for a new file format? Check out the CONTRIBUTING.rst docs.


License
=======

TODO
