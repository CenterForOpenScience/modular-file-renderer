.. _install:

Installation
============

mfr is actively developed on Github_.

You can clone the public repo: ::

    git clone https://github.com/CenterForOpenScience/modular-file-renderer.git

Or download one of the following:

* tarball_
* zipball_

Make sure that you have installed R, are using python3.5, and have installed invoke for your current python3 version.

Install the version of invoke found in the requirements.txt file. Currently 0.11.1

Install ``invoke``:

.. code-block:: bash

    pip install invoke==0.11.1

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

