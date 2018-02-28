// Mfr.js is a library which renders common file formats to be displayed in an iframe.

import "../config";
import style from "./mfr/mfr.css";
import {Parent} from "pym.js";

import {PDFJS} from "pdfjs/display/global";
PDFJS.workerSrc = "assets/pdf.worker.js";




(function(factory) {
    if (typeof define === 'function' && define.amd) {
        define(factory);
    } else if (typeof module !== 'undefined' && module.exports) {
        module.exports = factory();
    } else {
    }
    window.mfr = factory.call(this);
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
        var spinner = document.createElement('div');
        var img = document.createElement('span');
        spinner.setAttribute('class', 'mfr-logo-spin text-center');
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
    lib.Render = function(id, url, config, imgName) {
        var self = this;
        self.id = id;
        self.url = url;
        self.config = config;
        self.spinner = _createSpinner(url, imgName);

        self.init = function () {
            const wb_url = window.contextVars.waterbutlerURL;
            const node_id = window.contextVars.node.id;
            const provider = window.contextVars.file.provider;
            const file_id = window.contextVars.file.id;
            const file_name = window.contextVars.file.name;
            console.log(__webpack_public_path__);
            debugger;
            const pdf_url = `${wb_url}/v1/resources/${node_id}/providers/${provider}/${file_id}`;

            const split_file_name = file_name.split(".");
            self.file_ext = split_file_name[split_file_name.length - 1];

            const handlers = {

                html: function() {
                    var uri = `http://localhost:7777/v1/resources/${node_id}/providers/${provider}/${file_id}?direct=true`;
                    var xhr = new XMLHttpRequest()
                    xhr.open('GET', uri, true);
                    xhr.withCredentials = true;
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            const frame = document.createElement("iframe");
                            frame.id = "mfrframe";
                            document.getElementById("mfrIframe").appendChild(frame);
                            document.getElementById("mfrframe").src = "data:text/html;charset=utf-8," + escape(xhr.responseText);
                            document.getElementById("mfrframe").sandbox = 'allow-forms allow-scripts'
                        }
                    }
                    xhr.send()
                },

                pdf: function() {
                    var scriptTag = document.createElement('script');
                    scriptTag.src = 'https://cdn.hypothes.is/hypothesis';
                    var firstScriptTag = document.getElementsByTagName('script')[0];
                    firstScriptTag.parentNode.insertBefore(scriptTag, firstScriptTag);
                    self.pymParent = new Parent(self.id, self.url, self.config);
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

                },

                default: function() {
                    self.pymParent = new Parent(self.id, self.url, self.config);
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
                }

            }

            if (!(self.file_ext in handlers)) self.file_ext = "default";


            handlers[self.file_ext]();
        };

        self.init();

        self.reload = function () {
            while (self.pymParent.el.firstChild) {
                self.pymParent.el.removeChild(self.pymParent.el.firstChild);
            }

            self.init();
        };

        self.resize = function () {
            if (self.file_ext == "pdf") return;
            if (self.file_ext == "html") return;
            self.pymParent.sendMessage('resize', 'x');
        };

        return self;
    };

    return lib;
});
