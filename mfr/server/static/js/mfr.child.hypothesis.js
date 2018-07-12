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

        // If a pdf is being rendered and MFR has provided a stable identifier, override the
        // documentFingerprint with it before loading the hypothes.is client.  The client
        // will use this ID to identify the document when fetching/saving annotations. Also
        // override the document title to the file name and the document url to the parent
        // window. This will not affect loading of the document, but will change how Hypothes.is
        // indexes the annotation.  Previously the title on h.is would just be `export` (the
        // path from the export url), and the linked url would point to the export/download url,
        // meaning the annotations could never be viewed in context.  By linking to the referrer,
        // the annotations can be viewed in the context of the preprint.
        if (window.PDFViewerApplication) {
            if (window.MFR_STABLE_ID) {
                window.PDFViewerApplication.documentFingerprint = window.MFR_STABLE_ID;
            }
            if (window.MFR_FILE_NAME) {
                window.PDFViewerApplication.documentInfo.Title = window.MFR_FILE_NAME;
                document.title = window.MFR_FILE_NAME;
            }
            window.PDFViewerApplication.url = document.referrer;
        }

        var script = window.document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://hypothes.is/embed.js';
        window.document.head.appendChild(script);
        window.document.body.classList.add('show-hypothesis');
        hypothesisLoaded = true;
    };
})();
