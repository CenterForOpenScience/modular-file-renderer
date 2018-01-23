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

    function _createSpinner(url, imgName) {
        var parser = document.createElement('a');
        parser.href = url;

        var spinner = document.createElement('div');
        var img = document.createElement('img');
        spinner.setAttribute('class', 'mfr-logo-spin text-center');
        imgName = imgName || 'loading.png';
        img.setAttribute('src', parser.protocol + '//' + parser.host + '/static/images/' + imgName);
        spinner.appendChild(img);
        return spinner;
    }

    /**
     * The Render file iframe widget
     *
     * @class Render
     * @param {String} id The id of the div into which the iframe will be rendered.
     * @param {String} url The url of the iframe source.
     * @param {Object} config Configuration to override the default settings.
     * @param {String} imgName The filename of an image in mfr/server/static/images/ to use as a loading spinner
     */
    lib.Render = function (id, url, config, imgName) {
        var self = this;
        self.id = id;
        self.url = url;
        self.config = config;
        self.spinner = _createSpinner(url, imgName);

        self.init = function () {
            self.pymParent = new pym.Parent(self.id, self.url, self.config);
            self.pymParent.iframe.setAttribute('allowfullscreen', '');
            self.pymParent.iframe.setAttribute('webkitallowfullscreen', '');
            self.pymParent.iframe.setAttribute('scrolling', 'yes');
            self.pymParent.iframe.setAttribute('sandbox', 'allow-scripts allow-popups allow-same-origin');

            self.pymParent.el.appendChild(self.spinner);
            $(self.pymParent.iframe).on('load', function () {
                self.pymParent.el.removeChild(self.spinner);
            });

            self.pymParent.onMessage('embed', function(message) {
                _addClass(self.pymParent.el, 'embed-responsive');
                _addClass(self.pymParent.el, message);
                _addClass(self.pymParent.iframe, 'embed-responsive-item');
            });

            self.pymParent.onMessage('location', function(message) {
                window.location = message;
            });
        };

        self.init();

        self.reload = function () {
            while (self.pymParent.el.firstChild) {
                self.pymParent.el.removeChild(self.pymParent.el.firstChild);
            }

            self.init();
        };

        self.resize = function () {
            self.pymParent.sendMessage('resize', 'x');
        };

        return self;
    };

    return lib;
});
