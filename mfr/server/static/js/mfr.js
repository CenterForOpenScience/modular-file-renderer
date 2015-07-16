/*! pym.js - v0.4.2 - 2015-04-24 */
!function(a){"function"==typeof define&&define.amd?define(a):"undefined"!=typeof module&&module.exports?module.exports=a():window.pym=a.call(this)}(function(){var a="xPYMx",b={},c=function(a){var b=new RegExp("[\\?&]"+a.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]")+"=([^&#]*)"),c=b.exec(location.search);return null===c?"":decodeURIComponent(c[1].replace(/\+/g," "))},d=function(a,b){return"*"===b.xdomain||a.origin.match(new RegExp(b.xdomain+"$"))?!0:void 0},e=function(b,c,d){var e=["pym",b,c,d];return e.join(a)},f=function(b){var c=["pym",b,"(\\S+)","(.+)"];return new RegExp("^"+c.join(a)+"$")},g=function(){for(var a=document.querySelectorAll("[data-pym-src]:not([data-pym-auto-initialized])"),c=a.length,d=0;c>d;++d){var e=a[d];e.setAttribute("data-pym-auto-initialized",""),""===e.id&&(e.id="pym-"+d);var f=e.getAttribute("data-pym-src"),g=e.getAttribute("data-pym-xdomain"),h={};g&&(h.xdomain=g),new b.Parent(e.id,f,h)}};return b.Parent=function(a,b,c){this.id=a,this.url=b,this.el=document.getElementById(a),this.iframe=null,this.settings={xdomain:"*"},this.messageRegex=f(this.id),this.messageHandlers={},c=c||{},this._constructIframe=function(){var a=this.el.offsetWidth.toString();this.iframe=document.createElement("iframe");var b="",c=this.url.indexOf("#");c>-1&&(b=this.url.substring(c,this.url.length),this.url=this.url.substring(0,c)),this.url.indexOf("?")<0?this.url+="?":this.url+="&",this.iframe.src=this.url+"initialWidth="+a+"&childId="+this.id+b,this.iframe.setAttribute("width","100%"),this.iframe.setAttribute("scrolling","no"),this.iframe.setAttribute("marginheight","0"),this.iframe.setAttribute("frameborder","0"),this.el.appendChild(this.iframe);var d=this;window.addEventListener("resize",function(){d.sendWidth()})},this._fire=function(a,b){if(a in this.messageHandlers)for(var c=0;c<this.messageHandlers[a].length;c++)this.messageHandlers[a][c].call(this,b)},this._processMessage=function(a){if(d(a,this.settings)){var b=a.data.match(this.messageRegex);if(!b||3!==b.length)return!1;var c=b[1],e=b[2];this._fire(c,e)}},this._onHeightMessage=function(a){var b=parseInt(a);this.iframe.setAttribute("height",b+"px")},this._onNavigateToMessage=function(a){document.location.href=a},this.onMessage=function(a,b){a in this.messageHandlers||(this.messageHandlers[a]=[]),this.messageHandlers[a].push(b)},this.sendMessage=function(a,b){this.el.getElementsByTagName("iframe")[0].contentWindow.postMessage(e(this.id,a,b),"*")},this.sendWidth=function(){var a=this.el.offsetWidth.toString();this.sendMessage("width",a)};for(var g in c)this.settings[g]=c[g];this.onMessage("height",this._onHeightMessage),this.onMessage("navigateTo",this._onNavigateToMessage);var h=this;return window.addEventListener("message",function(a){return h._processMessage(a)},!1),this._constructIframe(),this},b.Child=function(b){this.parentWidth=null,this.id=null,this.settings={renderCallback:null,xdomain:"*",polling:0},this.messageRegex=null,this.messageHandlers={},b=b||{},this.onMessage=function(a,b){a in this.messageHandlers||(this.messageHandlers[a]=[]),this.messageHandlers[a].push(b)},this._fire=function(a,b){if(a in this.messageHandlers)for(var c=0;c<this.messageHandlers[a].length;c++)this.messageHandlers[a][c].call(this,b)},this._processMessage=function(a){if(d(a,this.settings)){var b=a.data.match(this.messageRegex);if(b&&3===b.length){var c=b[1],e=b[2];this._fire(c,e)}}},this._onWidthMessage=function(a){var b=parseInt(a);b!==this.parentWidth&&(this.parentWidth=b,this.settings.renderCallback&&this.settings.renderCallback(b),this.sendHeight())},this.sendMessage=function(a,b){window.parent.postMessage(e(this.id,a,b),"*")},this.sendHeight=function(){var a=document.getElementsByTagName("body")[0].offsetHeight.toString();h.sendMessage("height",a)},this.scrollParentTo=function(a){this.sendMessage("navigateTo","#"+a)},this.navigateParentTo=function(a){this.sendMessage("navigateTo",a)},this.id=c("childId")||b.id,this.messageRegex=new RegExp("^pym"+a+this.id+a+"(\\S+)"+a+"(.+)$");var f=parseInt(c("initialWidth"));this.onMessage("width",this._onWidthMessage);for(var g in b)this.settings[g]=b[g];var h=this;return window.addEventListener("message",function(a){h._processMessage(a)},!1),this.settings.renderCallback&&this.settings.renderCallback(f),this.sendHeight(),this.settings.polling&&window.setInterval(this.sendHeight,this.settings.polling),this},g(),b});

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

    function _createSpinner(url) {
        var parser = document.createElement('a');
        parser.href = url;

        var spinner = document.createElement('div');
        var img = document.createElement('img');
        spinner.setAttribute('class', 'mfr-logo-spin text-center');
        img.setAttribute('src', parser.protocol + '//' + parser.host + '/static/images/loading.png');
        spinner.appendChild(img);
        return spinner
    }

    /**
     * The Render file iframe widget
     *
     * @class Render
     * @param {String} id The id of the div into which the iframe will be rendered.
     * @param {String} url The url of the iframe source.
     * @param {Object} config Configuration to override the default settings.
     */
    lib.Render = function (id, url, config) {
        var self = this;
        self.id = id;
        self.url = url;
        self.config = config;
        self.spinner = _createSpinner(url);

        self.init = function () {
            self.pymParent = new pym.Parent(self.id, self.url, self.config);
            self.pymParent.iframe.setAttribute('allowfullscreen', '');
            self.pymParent.iframe.setAttribute('webkitallowfullscreen', '');

            self.pymParent.el.appendChild(self.spinner);
            $(self.pymParent.iframe).load(function () {
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
