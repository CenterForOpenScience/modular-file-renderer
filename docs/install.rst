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

This will install mfr and its core modules. Each module may have its own requirements and they be installed using the CLI::

    # install all plugin requirements
    mfr install all

    # install requirements for a specific core module
    mfr install mfr_code_pygments

Additionally, the ``[-e | -r]`` flags will install only exporter or render requirements, respectively::

    # install all render requirements
    mfr -r install all

You can alternatively install the requirements by passing the -requirements.txt file to pip::
	
	# install render-requirements for specific core module
	pip install -r /path/to/mfr_code_pygments/render-requirements.txt

.. _Github: https://github.com/CenterForOpenScience/modular-file-renderer
.. _tarball: https://github.com/CenterForOpenScience/modular-file-renderer/tarball/master
.. _zipball: https://github.com/CenterForOpenScience/modular-file-renderer/zipball/master
