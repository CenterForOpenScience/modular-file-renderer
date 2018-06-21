***********************
Contributing guidelines
***********************

- `PEP 8`_, when sensible.
- Test-driven: test ruthlessly and write docs for new features.
- Human-driven: make sure any new logic is easy for others to understand.
- If you add an extension to setup.py, add it to ``supportedextensions.md``.
- Please update ``AUTHORS.rst`` when you contribute.

.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/

Setting up for development
==========================

Clone the repo:

.. code-block:: bash

    $ git clone https://github.com/CenterForOpenScience/modular-file-renderer.git
    $ cd modular-file-renderer

Configure development environment and install the development dependencies.

.. note::
    Python 3.5 or greater, `R`_, and `pspp`_ are required.
    Python 3.6 is reccomended. It's recommended that a python version manager such as `pyenv`_ is used and that you use a virtual environment such as `pyenv-virtualenv`_ during development.

.. _R: https://www.r-project.org/
.. _pspp: https://www.gnu.org/software/pspp/
.. _pyenv: https://github.com/pyenv/pyenv
.. _pyenv-virtualenv: https://github.com/pyenv/pyenv-virtualenv

For Mac OS, here is an example of the commands that might be run to set up MFR. Linux users will probably do the same thing but with a different package manager. If someone wants to update this guide, please do.

.. code-block:: bash

    $ brew install r pspp
    $ pyenv virtualenv 3.6.4 mfr && echo mfr > .python-version
    $ pip install setuptools==30.4.0
    $ pip install invoke==0.13.0

Lastly, install MFR requirements with the development option.

.. code-block:: bash

    $ inv install -d
    $ inv server

Running tests
=============

To run all tests (requires ``pytest``)

.. code-block:: bash

    $ inv test

You can also use ``pytest`` directly.

.. code-block:: bash

    $ py.test --cov-report term-missing --cov mfr tests

Writing tests
=============

Unit tests should be written for all rendering code.

Tests should be encapsulated within a class and written as functions. There are a few `pytest fixtures`_ to help you mock files. You can use them by simply including them as parameters to your test functions.

.. code-block:: python

    # in test_myformat.py

    from mfr.extensions.my_extension.render import MyExtensionRenderer

    @pytest.fixture
    def metadata():
        return ProviderMetadata(
            'file_name',
            '.extension',
            'text/plain',
            '1234',
            'http://wb.osf.io/file/file_name.extension?token=1234'
        )

    def test_render_html(extension, metadata, file_path, assets_url, export_url):
        assert MyExtensionRenderer(
            extension,
            file_metadata,
            file_path,
            assets_url
        ).render() == '<p>Rendered file for my_extension</p>'

Check out `pytest`_ documentation to learn more about fixtures

.. _pytest fixtures: https://docs.pytest.org/en/latest/fixture.html
.. _pytest: https://docs.pytest.org/en/latest/

Manual Local Testing
====================

To make sure a new renderer is functioning properly, it's recommended that you try to render a file of that type locally. The easiest way to do this would be to use the ``docker-compose`` files available inside the osf repository to get the MFR running, and then it should be straightforward to interact with the service using a tool such as postman. Alternatively, if you are familiar with OSF and its services, you can run full OSF and render files directly with it.

Writing an extension
====================

An extension provides a 'renderer' and/or an 'exporter', and is registered in setup.py to allow the plugin to load when it is needed. Renderers and exporters subclasses ``mfr.core.extension.BaseRenderer`` or ``mfr.core.extension.BaseExporter`` respectively. A renderer takes a file path and some file metadata and returns a string of HTML that provides a representation of the file. The logic for the rendering happens in a renderer's ``render()`` function. This is an abstract base class method, and thus is required for the implementation of a renderer. Similarly, ``BaseExporter`` has an ``export()`` method. This method should take a file and convert it to the desired output, and create the newly converted file at the ``ouput_file_path``.

Renderers have an abstract property ``file_required``. This is used to determine if the renderer needs the actual content of the file in order to render it. Renderers also have a property ``cache_result``; this is used to determine whether the ouput of the renderer may be cached to improve future requests for the rendered version of the file.

Rendering Code
--------------

Renderers subclass ``mfr.core.extension.BaseRenderer``, and implement a render function, a ``file_required`` property, and a ``cache_result`` property.

.. code-block:: python

    import os

    from mako.lookup import TemplateLookup

    from mfr.core import extension


    class ImageRenderer(extension.BaseRenderer):

        TEMPLATE = TemplateLookup(
            directories=[
                os.path.join(os.path.dirname(__file__), 'templates')
            ]).get_template('viewer.mako')

        def render(self):
            return self.TEMPLATE.render(base=self.assets_url, url=self.url.geturl())

        @property
        def file_required(self):
            return False

        @property
        def cache_result(self):
            return False

Organization
------------

Each plugin has its own directory. At a minimum, a plugin should include:

- ``__init__.py``: This should export the ``mfr.core.extensions.BaseExporter`` and ``mfr.core.extensions.BaseRenderer`` subclasses provided by the plugin

A typical extension plugin directory structure might look like this:

::

	modular-file-renderer
	├── mfr
	│	├── __init__.py
	│	└── extensions
	│		├── __init__.py
	│		└── custom-plugin
	│			├── __init__.py
	│			├── render.py
	│			├── export.py
	│			├── settings.py
	│			├── static
	│			│	├── css
	│			│	└── js
	│			├── templates
	│			│	└── viewer.mako
	│			└── libs
	│				├── __init__.py
	│				└── tools.py
	├── tests
	│	├── __init__.py
	│	└── extensions
	│		├── __init__.py
	│		└── custom-plugin
	│			├── __init__.py
	│			└── test_custom_plugin.py
	├── setup.py
	├── README.md
	└── requirements.txt


Documentation
=============

Contributions to the documentation are welcome. Documentation is written in `reStructured Text`_ (rST). A quick rST reference can be found `here <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_. Builds are powered by Sphinx_.

To build docs: ::

    $ pip install -r doc-requirements.txt
    $ cd docs
    $ make html
    $ open _build/html/index.html

The ``-b`` (for "browse") automatically opens up the docs in your browser after building.

.. _Sphinx: http://sphinx.pocoo.org/

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
