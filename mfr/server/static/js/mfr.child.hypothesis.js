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

        var script = window.document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://hypothes.is/embed.js';
        window.document.head.appendChild(script);
        window.document.body.classList.add('show-hypothesis');
        hypothesisLoaded = true;
    };
})();
