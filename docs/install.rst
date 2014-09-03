.. _install:

Installation
============

mfr is actively developed on Github_.

You can clone the public repo: ::

    git clone https://github.com/CenterForOpenScience/modular-file-renderer.git

Or download one of the following:

* tarball_
* zipball_

Once you have the source, you can install it into your site-packages with ::

    $ python setup.py install

This will install mfr and its core modules. Each module may have its own requirements and they be installed using the cli::

    # install all plugin requirements
    mfr_install

    # install requirements for a specific core module
    mfr_install mfr_code_pygments

Additionally, ``mfr_install [-e | -r]`` installs only exporter or render requirements.

.. _Github: https://github.com/CenterForOpenScience/modular-file-renderer
.. _tarball: https://github.com/CenterForOpenScience/modular-file-renderer/tarball/master
.. _zipball: https://github.com/CenterForOpenScience/modular-file-renderer/zipball/master
