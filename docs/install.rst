.. _install:

Installation
============

mfr is actively developed on Github_.

You can clone the public repo: ::

    git clone https://github.com/CenterForOpenScience/modular-file-renderer.git

Or download one of the following:

* tarball_
* zipball_

Make sure that you have installed `pspp <https://www.gnu.org/software/pspp/>`_ and are using python 3.5 or greater.

Install the versions of ``setuptools`` and ``invoke`` found in the requirements.txt file:

.. code-block:: bash

    pip install setuptools==37.0.0
    pip install invoke==0.13.0

Install requirements:

.. code-block:: bash

    invoke install

Or for some nicities (like tests):

.. code-block:: bash

    invoke install --develop

Start the server:

.. note

    The server is extremely tenacious thanks to stevedore and tornado
    Syntax errors in the :mod:`mfr.providers` will not crash the server
    In debug mode the server will automatically reload

.. code-block:: bash

    invoke server

.. _Github: https://github.com/CenterForOpenScience/modular-file-renderer
.. _tarball: https://github.com/CenterForOpenScience/modular-file-renderer/tarball/master
.. _zipball: https://github.com/CenterForOpenScience/modular-file-renderer/zipball/master

