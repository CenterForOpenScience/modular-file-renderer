;(function() {
    'use strict';
    window.pymChild = new pym.Child();

    window.addEventListener('load', function () {
        window.pymChild.sendHeight();

        var anchors = document.getElementsByTagName('a');
        Array.prototype.slice.call(anchors).forEach(function (el) {
            el.addEventListener('click', function (e) {
                if (this.href !== undefined &&
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
})();
