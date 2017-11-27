/*! pym.js - v1.3.1 - 2017-07-25 */
!function(a){"function"==typeof define&&define.amd?define(a):"undefined"!=typeof module&&module.exports?module.exports=a():window.pym=a.call(this)}(function(){var a="xPYMx",b={},c=function(a){var b=document.createEvent("Event");b.initEvent("pym:"+a,!0,!0),document.dispatchEvent(b)},d=function(a){var b=new RegExp("[\\?&]"+a.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]")+"=([^&#]*)"),c=b.exec(location.search);return null===c?"":decodeURIComponent(c[1].replace(/\+/g," "))},e=function(a,b){if(("*"===b.xdomain||a.origin.match(new RegExp(b.xdomain+"$")))&&"string"==typeof a.data)return!0},f=function(b,c,d){var e=["pym",b,c,d];return e.join(a)},g=function(b){var c=["pym",b,"(\\S+)","(.*)"];return new RegExp("^"+c.join(a)+"$")},h=Date.now||function(){return(new Date).getTime()},i=function(a,b,c){var d,e,f,g=null,i=0;c||(c={});var j=function(){i=c.leading===!1?0:h(),g=null,f=a.apply(d,e),g||(d=e=null)};return function(){var k=h();i||c.leading!==!1||(i=k);var l=b-(k-i);return d=this,e=arguments,l<=0||l>b?(g&&(clearTimeout(g),g=null),i=k,f=a.apply(d,e),g||(d=e=null)):g||c.trailing===!1||(g=setTimeout(j,l)),f}},j=function(){for(var a=b.autoInitInstances.length,c=a-1;c>=0;c--){var d=b.autoInitInstances[c];d.el.getElementsByTagName("iframe").length&&d.el.getElementsByTagName("iframe")[0].contentWindow||b.autoInitInstances.splice(c,1)}};return b.autoInitInstances=[],b.autoInit=function(a){var d=document.querySelectorAll("[data-pym-src]:not([data-pym-auto-initialized])"),e=d.length;j();for(var f=0;f<e;++f){var g=d[f];g.setAttribute("data-pym-auto-initialized",""),""===g.id&&(g.id="pym-"+f+"-"+Math.random().toString(36).substr(2,5));var h=g.getAttribute("data-pym-src"),i={xdomain:"string",title:"string",name:"string",id:"string",sandbox:"string",allowfullscreen:"boolean",parenturlparam:"string",parenturlvalue:"string",optionalparams:"boolean",trackscroll:"boolean",scrollwait:"number"},k={};for(var l in i)if(null!==g.getAttribute("data-pym-"+l))switch(i[l]){case"boolean":k[l]=!("false"===g.getAttribute("data-pym-"+l));break;case"string":k[l]=g.getAttribute("data-pym-"+l);break;case"number":var m=Number(g.getAttribute("data-pym-"+l));isNaN(m)||(k[l]=m);break;default:console.err("unrecognized attribute type")}var n=new b.Parent(g.id,h,k);b.autoInitInstances.push(n)}return a||c("pym-initialized"),b.autoInitInstances},b.Parent=function(a,b,c){this.id=a,this.url=b,this.el=document.getElementById(a),this.iframe=null,this.settings={xdomain:"*",optionalparams:!0,parenturlparam:"parentUrl",parenturlvalue:window.location.href,trackscroll:!1,scrollwait:100},this.messageRegex=g(this.id),this.messageHandlers={},c=c||{},this._constructIframe=function(){var a=this.el.offsetWidth.toString();this.iframe=document.createElement("iframe");var b="",c=this.url.indexOf("#");for(c>-1&&(b=this.url.substring(c,this.url.length),this.url=this.url.substring(0,c)),this.url.indexOf("?")<0?this.url+="?":this.url+="&",this.iframe.src=this.url+"initialWidth="+a+"&childId="+this.id,this.settings.optionalparams&&(this.iframe.src+="&parentTitle="+encodeURIComponent(document.title),this.iframe.src+="&"+this.settings.parenturlparam+"="+encodeURIComponent(this.settings.parenturlvalue)),this.iframe.src+=b,this.iframe.setAttribute("width","100%"),this.iframe.setAttribute("scrolling","no"),this.iframe.setAttribute("marginheight","0"),this.iframe.setAttribute("frameborder","0"),this.settings.title&&this.iframe.setAttribute("title",this.settings.title),void 0!==this.settings.allowfullscreen&&this.settings.allowfullscreen!==!1&&this.iframe.setAttribute("allowfullscreen",""),void 0!==this.settings.sandbox&&"string"==typeof this.settings.sandbox&&this.iframe.setAttribute("sandbox",this.settings.sandbox),this.settings.id&&(document.getElementById(this.settings.id)||this.iframe.setAttribute("id",this.settings.id)),this.settings.name&&this.iframe.setAttribute("name",this.settings.name);this.el.firstChild;)this.el.removeChild(this.el.firstChild);this.el.appendChild(this.iframe),window.addEventListener("resize",this._onResize),this.settings.trackscroll&&window.addEventListener("scroll",this._throttleOnScroll)},this._onResize=function(){this.sendWidth(),this.settings.trackscroll&&this.sendViewportAndIFramePosition()}.bind(this),this._onScroll=function(){this.sendViewportAndIFramePosition()}.bind(this),this._fire=function(a,b){if(a in this.messageHandlers)for(var c=0;c<this.messageHandlers[a].length;c++)this.messageHandlers[a][c].call(this,b)},this.remove=function(){window.removeEventListener("message",this._processMessage),window.removeEventListener("resize",this._onResize),this.el.removeChild(this.iframe),j()},this._processMessage=function(a){if(e(a,this.settings)&&"string"==typeof a.data){var b=a.data.match(this.messageRegex);if(!b||3!==b.length)return!1;var c=b[1],d=b[2];this._fire(c,d)}}.bind(this),this._onHeightMessage=function(a){var b=parseInt(a);this.iframe.setAttribute("height",b+"px")},this._onNavigateToMessage=function(a){document.location.href=a},this._onScrollToChildPosMessage=function(a){var b=document.getElementById(this.id).getBoundingClientRect().top+window.pageYOffset,c=b+parseInt(a);window.scrollTo(0,c)},this.onMessage=function(a,b){a in this.messageHandlers||(this.messageHandlers[a]=[]),this.messageHandlers[a].push(b)},this.sendMessage=function(a,b){this.el.getElementsByTagName("iframe").length&&(this.el.getElementsByTagName("iframe")[0].contentWindow?this.el.getElementsByTagName("iframe")[0].contentWindow.postMessage(f(this.id,a,b),"*"):this.remove())},this.sendWidth=function(){var a=this.el.offsetWidth.toString();this.sendMessage("width",a)},this.sendViewportAndIFramePosition=function(){var a=this.iframe.getBoundingClientRect(),b=window.innerWidth||document.documentElement.clientWidth,c=window.innerHeight||document.documentElement.clientHeight,d=b+" "+c;d+=" "+a.top+" "+a.left,d+=" "+a.bottom+" "+a.right,this.sendMessage("viewport-iframe-position",d)};for(var d in c)this.settings[d]=c[d];return this._throttleOnScroll=i(this._onScroll.bind(this),this.settings.scrollwait),this.onMessage("height",this._onHeightMessage),this.onMessage("navigateTo",this._onNavigateToMessage),this.onMessage("scrollToChildPos",this._onScrollToChildPosMessage),this.onMessage("parentPositionInfo",this.sendViewportAndIFramePosition),window.addEventListener("message",this._processMessage,!1),this._constructIframe(),this},b.Child=function(b){this.parentWidth=null,this.id=null,this.parentTitle=null,this.parentUrl=null,this.settings={renderCallback:null,xdomain:"*",polling:0,parenturlparam:"parentUrl"},this.timerId=null,this.messageRegex=null,this.messageHandlers={},b=b||{},this.onMessage=function(a,b){a in this.messageHandlers||(this.messageHandlers[a]=[]),this.messageHandlers[a].push(b)},this._fire=function(a,b){if(a in this.messageHandlers)for(var c=0;c<this.messageHandlers[a].length;c++)this.messageHandlers[a][c].call(this,b)},this._processMessage=function(a){if(e(a,this.settings)&&"string"==typeof a.data){var b=a.data.match(this.messageRegex);if(b&&3===b.length){var c=b[1],d=b[2];this._fire(c,d)}}}.bind(this),this._onWidthMessage=function(a){var b=parseInt(a);b!==this.parentWidth&&(this.parentWidth=b,this.settings.renderCallback&&this.settings.renderCallback(b),this.sendHeight())},this.sendMessage=function(a,b){window.parent.postMessage(f(this.id,a,b),"*")},this.sendHeight=function(){var a=document.getElementsByTagName("body")[0].offsetHeight.toString();return this.sendMessage("height",a),a}.bind(this),this.getParentPositionInfo=function(){this.sendMessage("parentPositionInfo")},this.scrollParentTo=function(a){this.sendMessage("navigateTo","#"+a)},this.navigateParentTo=function(a){this.sendMessage("navigateTo",a)},this.scrollParentToChildEl=function(a){var b=document.getElementById(a).getBoundingClientRect().top+window.pageYOffset;this.scrollParentToChildPos(b)},this.scrollParentToChildPos=function(a){this.sendMessage("scrollToChildPos",a.toString())};var g=function(a){var b,d=document.getElementsByTagName("html")[0],e=d.className;try{b=window.self!==window.top?"embedded":"not-embedded"}catch(a){b="embedded"}e.indexOf(b)<0&&(d.className=e?e+" "+b:b,a&&a(b),c("marked-embedded"))};this.remove=function(){window.removeEventListener("message",this._processMessage),this.timerId&&clearInterval(this.timerId)};for(var h in b)this.settings[h]=b[h];this.id=d("childId")||b.id,this.messageRegex=new RegExp("^pym"+a+this.id+a+"(\\S+)"+a+"(.*)$");var i=parseInt(d("initialWidth"));return this.parentUrl=d(this.settings.parenturlparam),this.parentTitle=d("parentTitle"),this.onMessage("width",this._onWidthMessage),window.addEventListener("message",this._processMessage,!1),this.settings.renderCallback&&this.settings.renderCallback(i),this.sendHeight(),this.settings.polling&&(this.timerId=window.setInterval(this.sendHeight,this.settings.polling)),g(b.onMarkedEmbeddedStatus),this},"undefined"!=typeof document&&b.autoInit(!0),b});
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

    function _createSpinner() {
        // The the OSF asks for the CSS for this spinner (/static/css/mfr)
        // MFR itself does not use it anywhere
        var spinner = document.createElement('div');
        spinner.setAttribute('class', 'ball-pulse ball-dark text-center');
        for(i=0; i < 3; i++){
            spinner.appendChild(document.createElement('div'));
        }

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
        // we no longer use this, but need to support it as an arg till the OSF side is fixed
        imgName = undefined;
        var self = this;
        self.id = id;
        self.url = url;
        self.config = config;
        self.spinner = _createSpinner();

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
