Setting Up
==========

Make sure that you have installed R, are using python3.5, and have installed invoke for your current python3 version.

Install ``invoke``:

.. code-block:: bash

    pip install invoke

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
