;(function() {
    'use strict';
    window.pymChild = new pym.Child();

    window.onload = function () {
        window.pymChild.sendHeight();
    };

    window.onresize = function() {
        window.pymChild.sendHeight();
    };

    window.pymChild.onMessage('reload', function () {
        window.location.reload();
    });

    window.pymChild.onMessage('resize', function () {
        window.pymChild.sendHeight();
    });
})();
