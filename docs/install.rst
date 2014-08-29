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

This will install mfr and its core modules. Each module may have its own requirements and they be installed using invoke: ::

    # install all plugin requirements
    invoke plugin_requirements

    # install requirements for a specific core module
    invoke plugin_requirements -p mfr_code_pygments

Additionally, ``invoke plugin_requirements [-e | -r]`` installs only exporter or render requirements.

To use an external plugin, simply install it into your virtual environment. You will then have to register the new file handler using either a config document (see Examples) or inline (see Quickstart).

.. _Github: https://github.com/CenterForOpenScience/modular-file-renderer
.. _tarball: https://github.com/CenterForOpenScience/modular-file-renderer/tarball/master
.. _zipball: https://github.com/CenterForOpenScience/modular-file-renderer/zipball/master
