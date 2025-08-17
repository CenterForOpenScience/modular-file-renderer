.. _install:

Installation
============

mfr is actively developed on Github_.

You can clone the public repo: ::

    git clone https://github.com/CenterForOpenScience/modular-file-renderer.git

Or download one of the following:

* tarball_
* zipball_

Make sure that you have installed `pspp <https://www.gnu.org/software/pspp/>`_ and are using python v3.13 or greater.

Install ``poetry`` to manage dependencies:

.. code-block:: bash

    pip install poetry==2.1.2

Install requirements:

.. code-block:: bash

    poetry install

Or for some nicities (like tests):

.. code-block:: bash

    poetry install --with dev

Start the server:

.. note

    The server is extremely tenacious thanks to stevedore and tornado
    Syntax errors in the :mod:`mfr.providers` will not crash the server
    In debug mode the server will automatically reload

.. code-block:: bash

    poetry run invoke server

.. _Github: https://github.com/CenterForOpenScience/modular-file-renderer
.. _tarball: https://github.com/CenterForOpenScience/modular-file-renderer/tarball/master
.. _zipball: https://github.com/CenterForOpenScience/modular-file-renderer/zipball/master

