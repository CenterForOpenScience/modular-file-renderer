;(function() {
    'use strict';

    window.pymChild = new pym.Child();

    window.addEventListener('load', function () {
        window.pymChild.sendHeight();

        var anchors = document.getElementsByTagName('a');
        Array.prototype.slice.call(anchors).forEach(function (el) {
            el.addEventListener('click', function (e) {
                if (this.href !== undefined &&
                    this.href !== "" &&
                    this.href[0] !== '#') {
                    e.preventDefault();
                    window.pymChild.sendMessage('location', this.href);
                }
            });
        });
    });

    window.addEventListener('resize', function () {
        window.pymChild.sendHeight();
    });

    window.pymChild.onMessage('resize', function () {
        window.pymChild.sendHeight();
    });

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
