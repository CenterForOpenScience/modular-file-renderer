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
        // will use this ID to identify the document when fetching/saving annotations.
        if (window.MFR_STABLE_ID && window.PDFViewerApplication) {
            window.PDFViewerApplication.documentFingerprint = window.MFR_STABLE_ID;
        }

        var script = window.document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://hypothes.is/embed.js';
        window.document.head.appendChild(script);
        window.document.body.classList.add('show-hypothesis');
        hypothesisLoaded = true;
    };
})();
