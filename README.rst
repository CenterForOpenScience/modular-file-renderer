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


License
=======

TODO
