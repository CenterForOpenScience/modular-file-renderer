;(function() {
    'use strict';
    window.pymChild = new pym.Child();

    window.onload = function(e) {
        window.pymChild.sendHeight();
    };

    window.pymChild.onMessage('reload', function() {
        window.location.reload();
    });
})();
