Contributing guidelines
=======================

In General
----------

- `PEP 8`_, when sensible.
- Test ruthlessly. Write docs for new features.
- Even more important than Test-Driven Development--*Human-Driven Development*.

.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/


Setting up for development
--------------------------

TODO


Running tests
-------------

To run all tests (requires pytest) ::

    $ invoke test

You can also use pytest directly. ::

    $ py.test


Using the previewer
-------------------

The mfr comes with a Flask app for previewing rendered files.

To run the app, run: ::

    $ invoke previewer

Then browse to ``localhost:5000`` in your browser.
