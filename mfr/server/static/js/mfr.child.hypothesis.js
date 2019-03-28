;(function() {
    'use strict';

    var hypothesisLoaded = false;

    window.pymChild.onMessage('startHypothesis', startHypothesis);

    window.addEventListener('message', function(event) {
        if (event.data === 'startHypothesis') {
            startHypothesis(event);
        }
    });

    function startHypothesis(event) {
        if (hypothesisLoaded) {
            return;
        }

        // 'pagerendered' is an event emitted by pdf.js after the file metadata has been loaded and
        // the first page rendered.  We must delay setting the fake metadata until after the
        // document has been loaded, or pdf.js will overwrite our fake metadata with the real
        // metadata.
        document.addEventListener('pagerendered', function(e) {

            // Changes made here will not affect loading of the document, but will change how
            // Hypothes.is indexes the annotations.

            // If a pdf is being rendered and MFR has provided a stable identifier, override the
            // documentFingerprint with it before loading the hypothes.is client.  The client
            // will use this ID to identify the document when fetching/saving annotations.
            if (window.MFR_STABLE_ID) {
                // pdf.js uses the first property to set the second. Set both for now, just to be
                // safe. The second will be going away in a future pdf.js release.
                window.PDFViewerApplication.pdfDocument.pdfInfo.fingerprint = window.MFR_STABLE_ID;
                window.PDFViewerApplication.documentFingerprint = window.MFR_STABLE_ID;
            }

            // Override the document title to the file name and the document url to the parent
            // window. This will not affect loading of the document, but will change how Hypothes.is
            // indexes the annotation.  Previously, the page title on h.is would be the final path
            // part of the download url, which would be an opaque file identifier or just `export`.
            if (window.MFR_FILE_NAME) {
                if (window.PDFViewerApplication.documentInfo) {
                    window.PDFViewerApplication.documentInfo.Title = window.MFR_FILE_NAME;
                }
                else {
                    window.PDFViewerApplication.documentInfo = {"Title": window.MFR_FILE_NAME};
                }
                document.title = window.MFR_FILE_NAME;
            }

            // Override the document url to point to the parent window. Before, the linked url would
            // point to the export/download url, meaning the annotations could never be viewed in
            // context.  By linking to the referrer, the annotations can be viewed in the context of
            // the preprint.
            window.PDFViewerApplication.url = document.referrer;

            // Load the hypothes.is client
            var script = window.document.createElement('script');
            script.type = 'text/javascript';
            script.src = 'https://hypothes.is/embed.js';
            window.document.head.appendChild(script);
            window.document.body.classList.add('show-hypothesis');
            hypothesisLoaded = true;

            var sidePanelOpened = false;
            // window.DEFAULT_URL should be the wb link in this format:
            // https://<wb-domain>/v1/resources/<preprint-guid>/providers/osfstorage/<file-id>?direct=&mode=render
            // TODO: parse and validate the WB URL before retrieving the preprints GUID
            var wbLink = window.DEFAULT_URL;
            var preprintGuid;
            if (wbLink.split('/').length >= 6) {
                preprintGuid = wbLink.split('/')[5];
            } else {
                preprintGuid = 'preprint-guid-unknown';
            }
            var sendAnalyticsIfExpanded = function (expanded) { 
                if (expanded && !sidePanelOpened) {
                    sidePanelOpened = expanded;
                    ga('send', 'event', {
                        eventCategory: 'Hypothesis',
                        eventAction: 'Open Hypothesis Panel',
                        //`eventLabel` is the guid of the preprint to which the file belongs
                        eventLabel: preprintGuid,
                    });
                }
            };
            window.hypothesisConfig = function () {
                return {
                  "onLayoutChange": function (layout) { return sendAnalyticsIfExpanded(layout.expanded); }
                };
            };
        });
    };
})();
