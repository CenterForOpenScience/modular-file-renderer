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

Clone the repo: ::

    $ git clone https://github.com/CenterForOpenScience/modular-file-renderer.git
    $ cd modular-file-renderer

Install the development dependencies. ::

    $ pip install -r dev-requirements.txt


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


Documentation
-------------

Contributions to the documentation are welcome. Documentation is written in `reStructured Text`_ (rST). A quick rST reference can be found `here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_. Builds are powered by Sphinx_.

To build docs: ::

    $ invoke docs -b

The ``-b`` (for "browse") automatically opens up the docs in your browser after building.

.. _Sphinx: http://sphinx.pocoo.org/

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
