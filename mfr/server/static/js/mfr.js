/*
* Mfr.js is a library which renders common file formats to be displayed in an iframe.
*/

(function(factory) {
    if (typeof define === 'function' && define.amd) {
        define(factory);
    } else if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
        window.mfr = factory.call(this);
    }
})(function() {
    var lib = {};

    function _hasClass(el, className) {
        if (el.classList) {
            return el.classList.contains(className);
        } else {
            return (-1 < el.className.indexOf(className));
        }
    }

    function _addClass(el, className) {
        if (el.classList) {
            el.classList.add(className);
        } else if (!_hasClass(el, className)) {
            var classes = el.className.split(' ');
            classes.push(className);
            el.className = classes.join(' ');
        }
        return el;
    }

    function _removeClass(el, className) {
        if (el.classList) {
            el.classList.remove(className);
        } else {
            var classes = el.className.split(' ');
            classes.splice(classes.indexOf(className), 1);
            el.className = classes.join(' ');
        }
        return el;
    }

    /**
     * The Render file iframe widget
     *
     * @class Render
     * @param {String} id The id of the div into which the iframe will be rendered.
     * @param {String} url The url of the iframe source.
     * @param {Object} config Configuration to override the default settings.
     */
    lib.Render = function(id, url, config) {
        var self = this;
        self.pymParent = new pym.Parent(id, url, config);
        self.pymParent.iframe.setAttribute('allowfullscreen', '');
        self.pymParent.iframe.setAttribute('webkitallowfullscreen', '');

        self.reload = function () {
            self.pymParent.sendMessage('reload', 'x');
        };

        self.pymParent.onMessage('embed', function(message) {
            _addClass(self.pymParent.el, 'embed-responsive');
            _addClass(self.pymParent.el, message);
            _addClass(self.pymParent.iframe, 'embed-responsive-item');
        });

        return self;
    };

    return lib;
});
