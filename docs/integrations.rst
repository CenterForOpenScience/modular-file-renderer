.. _integrations:

Integrations
============


Hypothes.is annotator
---------------------

MFR supports loading the `Hypothes.is <https://hypothes.is/>`_ annotation sidebar on pdfs and files converted to pdf.  Hypothes.is allows users to publicly comment and converse on internet-accesible files.  The annotator is not automatically loaded; it must be signaled to turn on by the parent iframe.  MFR also overrides some of the properties used by the sidebar to identify the annotation.  


Enabling
^^^^^^^^

The annotator is not loaded automatically for every MFR pdf render. The parent frame will need to send the ``startHypothesis`` event to the MFR iframe to start loading the annotator.  If the iframe is created via ``mfr.js``, then this signal can be sent by calling ``.startHypothesis()`` on the Render object.  If ``mfr.js`` is not used, then the signal can be sent by calling ``.postMessage()`` on the iframe:

.. code-block:: javascript

    $('iframe')[0].contentWindow.postMessage('startHypothesis', mfrUrl);

When the iframe receives this event, it will override the pdf.js metadata the annotator extracts then inject the hypothes.is loader script into the iframe.

Hypothes.is support can be completely disabled by setting the ``ENABLE_HYPOTHESIS`` flag to `False` in the pdf extension settings (`mfr.extensions.pdf.settings`). If running via the OSF's docker-compose, add ``PDF_EXTENSION_CONFIG_ENABLE_HYPOTHESIS=0`` to ``.docker-compose.mfr.env`` in the osf.io repo and recreate the container. If this flag is turned off, sending the ``startHypothesis`` event to the iframe will do nothing.


Annotator metadata
^^^^^^^^^^^^^^^^^^

The annotator client links annotations to both the url of the document and an identifier embedded in the pdf.  It also attaches the page title as metadata to the annotation. [#f1]_  In MFR, all three of these may be unsuitable for one reason or another, so MFR will override the properties that the client retrieves to provide more appropriate values.  These properties are:

**URL**: The MFR url can be complex, especially since it takes another url as a query parameter. Hypothes.is can handle reordering of the top-level parameters, but any change to the internal url will be taken as a new url, causing annotations to be lost. In addition, the url is used by hypothesis to provide share links and "view-in-context" links.  Visiting an MFR render url will load the iframe, but without an external frame to send the ``startHypothesis`` signal, the annotations will never be loaded.  Visiting an MFR export url will start a download of the document, with no chance of showing annotations.  Instead, MFR sets the annotation url to the parent frame, which is expected to be simpler and provide more context.

**Document ID**:  The document ID is an identifier embedded in the pdf.  pdf.js will extract this value, or if it is not present, return the md5 hash of the first 1024 bytes of data in the pdf.  User-provided pdfs will *usually* contain IDs, but may not. If the pdf is updated there is no guarantee that the ID will be preserved across revisions. If the ID changes, the document could lose its annotations.  pdfs exported by LibreOffice do not contain any identifiers and may change unpredictably.  For these reasons, MFR exports a stable identifier that should persist across revisions.  The stable ID is defined by the auth provider.  The OSF auth provider uses a hash of file metadata that is particular to that file and unlikely to change.  MFR does not modify the file, instead overwriting the identifier detected by pdf.js, which is then read by the annotator client.

**Title**: The annotator will derive the annotation page title from the pdf title. Similar to Document IDs, user-provided pdfs may or may not have a title.  LibreOffice-exported pdfs do not have an embedded title.  If an embedded title isn't found, the annotator will fall back to the iframe document's title, which if not set will default to the path part of the iframe url.  This results in annotation titles of "render" or "export", with no distinguishing attributes from other MFR annotations.  MFR works around this by updating the pdf.js-detected title and page title with the source file's name.

.. rubric:: Footnotes

.. [#f1] If the page title changes between annotations, the client will send the new page title with new annotations, but the hypothesis aggregator will discard that and `use the first title received <https://github.com/hypothesis/h/blob/8410ff35150ea600c02458e4558a67db7c926816/h/activity/bucketing.py#L27>`_ for that identifier.
