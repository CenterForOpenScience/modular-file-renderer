.. _overview:

Overview
========

Modular File Renderer (MFR) is a Python web application that provides a single interface for displaying many different types of files in a browser.  If an iframe's ``src`` attribute is an MFR render url, MFR will return the html needed to display the image, document, object, etc.

There are three main categories of modules in MFR: :ref:`Handlers <handlers>`, :ref:`Providers <providers>`, and :ref:`Extensions <extensions>`.  Handlers are the user-facing endpoints of MFR, accepting HTTP requests and returning either HTML or the file. Providers are responsible for knowing how to fetch the metadata and content for a file, given a URL to it.  Extensions convert files and construct HTML to make specific file types renderable in a browser.


.. _handlers:

Handlers
--------

In MFR, **handlers** are the classes that handle the web requests made to MFR.  The two most important handlers are the Render handler, which handles reequests to the ``/render`` endpoint, and the Export handler, which handles requests to the ``/export`` endpoint.  There are also endpoints for handling static assets, but those will not be described here.  See `mfr.server.app` and `mfr.server.core.ExtensionsStaticFileHandler` for those.

Base handler
^^^^^^^^^^^^

The **base handler** extracts the ``url`` query parameter from the request, constructs an appropriate MFR Provider object, then asks the Provider to fetch the file metadata.

Render handler
^^^^^^^^^^^^^^

The **Render handler** will construct an appropriate renderer using the Extension module that is mapped to the file's extension.  Some renderers require the file contents be inserted inline (ex. code snippets needing syntax highlighting).  Those will download the file via the Provider.  Others will only need a url to the file, which the Extension renderer will be responsible for inserting.  The output from the renderer will be cached if caching is enabled.


Export handler
^^^^^^^^^^^^^^

The **Export handler** takes the ``url`` to the file and a ``format`` query parameter, and constructs an Extension exporter to convert the file into the requested format.  For example, most browsers can't render ``.docx`` files directly, so the Extension exporter will convert it to a PDF.  The Export handler can also cache results if caching is enabled.


.. _providers:

Providers
---------

The **Provider** is responsible for knowing how to take a url to a file and get both the content and metadata for that file.

Base provider
^^^^^^^^^^^^^

Does little except verifying that the url is hosted at a supported domain.

HTTP provider
^^^^^^^^^^^^^

Naive provider that infers file metadata (extension, type, etc.) from the url.  Downloads by issuing GET request against the url.

OSF provider
^^^^^^^^^^^^

`Open Science Framework <https://osf.io/>`_ -aware provider that can convert the given url into a WaterButler url.  WaterButler is a file action abstraction service that can be used to fetch metadata and download file contents.  The OSF provider also knows how to pass through OSF credentials, to enforce read-access restrictions.


.. _extensions:

Extensions
----------

**Extensions** are the modules that generate the HTML needed to render a given file type.  They may also provide exporters if the file's native type is unrenderable and needs to be converted to another format suitable for browsers.  Extension renderers inherit from `mfr.core.extension.BaseRenderer` and exporters inherit from `mfr.core.extension.BaseExporter`.
