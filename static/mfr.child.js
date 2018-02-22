/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 216);
/******/ })
/************************************************************************/
/******/ ({

/***/ 134:
/***/ (function(module, exports, __webpack_require__) {

"use strict";
var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_RESULT__;

(function (factory) {
  if (true) {
    !(__WEBPACK_AMD_DEFINE_FACTORY__ = (factory),
				__WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ?
				(__WEBPACK_AMD_DEFINE_FACTORY__.call(exports, __webpack_require__, exports, module)) :
				__WEBPACK_AMD_DEFINE_FACTORY__),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
  } else if (typeof module !== 'undefined' && module.exports) {
    module.exports = factory();
  } else {
    window.pym = factory.call(this);
  }
})(function () {
  var MESSAGE_DELIMITER = 'xPYMx';
  var lib = {};
  var _raiseCustomEvent = function _raiseCustomEvent(eventName) {
    var event = document.createEvent('Event');
    event.initEvent('pym:' + eventName, true, true);
    document.dispatchEvent(event);
  };
  var _getParameterByName = function _getParameterByName(name) {
    var regex = new RegExp("[\\?&]" + name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]') + '=([^&#]*)');
    var results = regex.exec(location.search);
    if (results === null) {
      return '';
    }
    return decodeURIComponent(results[1].replace(/\+/g, " "));
  };
  var _isSafeMessage = function _isSafeMessage(e, settings) {
    if (settings.xdomain !== '*') {
      if (!e.origin.match(new RegExp(settings.xdomain + '$'))) {
        return;
      }
    }
    if (typeof e.data !== 'string') {
      return;
    }
    return true;
  };
  var _isSafeUrl = function _isSafeUrl(url) {
    var SAFE_URL_PATTERN = /^(?:(?:https?|mailto|ftp):|[^&:/?#]*(?:[/?#]|$))/gi;
    if (!url.match(SAFE_URL_PATTERN)) {
      return;
    }
    return true;
  };
  var _makeMessage = function _makeMessage(id, messageType, message) {
    var bits = ['pym', id, messageType, message];
    return bits.join(MESSAGE_DELIMITER);
  };
  var _makeMessageRegex = function _makeMessageRegex(id) {
    var bits = ['pym', id, '(\\S+)', '(.*)'];
    return new RegExp('^' + bits.join(MESSAGE_DELIMITER) + '$');
  };
  var _getNow = Date.now || function () {
    return new Date().getTime();
  };
  var _throttle = function _throttle(func, wait, options) {
    var context, args, result;
    var timeout = null;
    var previous = 0;
    if (!options) {
      options = {};
    }
    var later = function later() {
      previous = options.leading === false ? 0 : _getNow();
      timeout = null;
      result = func.apply(context, args);
      if (!timeout) {
        context = args = null;
      }
    };
    return function () {
      var now = _getNow();
      if (!previous && options.leading === false) {
        previous = now;
      }
      var remaining = wait - (now - previous);
      context = this;
      args = arguments;
      if (remaining <= 0 || remaining > wait) {
        if (timeout) {
          clearTimeout(timeout);
          timeout = null;
        }
        previous = now;
        result = func.apply(context, args);
        if (!timeout) {
          context = args = null;
        }
      } else if (!timeout && options.trailing !== false) {
        timeout = setTimeout(later, remaining);
      }
      return result;
    };
  };
  var _cleanAutoInitInstances = function _cleanAutoInitInstances() {
    var length = lib.autoInitInstances.length;
    for (var idx = length - 1; idx >= 0; idx--) {
      var instance = lib.autoInitInstances[idx];
      if (instance.el.getElementsByTagName('iframe').length && instance.el.getElementsByTagName('iframe')[0].contentWindow) {
        continue;
      } else {
        lib.autoInitInstances.splice(idx, 1);
      }
    }
  };
  lib.autoInitInstances = [];
  lib.autoInit = function (doNotRaiseEvents) {
    var elements = document.querySelectorAll('[data-pym-src]:not([data-pym-auto-initialized])');
    var length = elements.length;
    _cleanAutoInitInstances();
    for (var idx = 0; idx < length; ++idx) {
      var element = elements[idx];
      element.setAttribute('data-pym-auto-initialized', '');
      if (element.id === '') {
        element.id = 'pym-' + idx + "-" + Math.random().toString(36).substr(2, 5);
      }
      var src = element.getAttribute('data-pym-src');
      var settings = {
        'xdomain': 'string',
        'title': 'string',
        'name': 'string',
        'id': 'string',
        'sandbox': 'string',
        'allowfullscreen': 'boolean',
        'parenturlparam': 'string',
        'parenturlvalue': 'string',
        'optionalparams': 'boolean',
        'trackscroll': 'boolean',
        'scrollwait': 'number'
      };
      var config = {};
      for (var attribute in settings) {
        if (element.getAttribute('data-pym-' + attribute) !== null) {
          switch (settings[attribute]) {
            case 'boolean':
              config[attribute] = !(element.getAttribute('data-pym-' + attribute) === 'false');
              break;
            case 'string':
              config[attribute] = element.getAttribute('data-pym-' + attribute);
              break;
            case 'number':
              var n = Number(element.getAttribute('data-pym-' + attribute));
              if (!isNaN(n)) {
                config[attribute] = n;
              }
              break;
            default:
              console.err('unrecognized attribute type');
          }
        }
      }
      var parent = new lib.Parent(element.id, src, config);
      lib.autoInitInstances.push(parent);
    }
    if (!doNotRaiseEvents) {
      _raiseCustomEvent("pym-initialized");
    }
    return lib.autoInitInstances;
  };
  lib.Parent = function (id, url, config) {
    this.id = id;
    this.url = url;
    this.el = document.getElementById(id);
    this.iframe = null;
    this.settings = {
      xdomain: '*',
      optionalparams: true,
      parenturlparam: 'parentUrl',
      parenturlvalue: window.location.href,
      trackscroll: false,
      scrollwait: 100
    };
    this.messageRegex = _makeMessageRegex(this.id);
    this.messageHandlers = {};
    config = config || {};
    this._constructIframe = function () {
      var width = this.el.offsetWidth.toString();
      this.iframe = document.createElement('iframe');
      var hash = '';
      var hashIndex = this.url.indexOf('#');
      if (hashIndex > -1) {
        hash = this.url.substring(hashIndex, this.url.length);
        this.url = this.url.substring(0, hashIndex);
      }
      if (this.url.indexOf('?') < 0) {
        this.url += '?';
      } else {
        this.url += '&';
      }
      this.iframe.src = this.url + 'initialWidth=' + width + '&childId=' + this.id;
      if (this.settings.optionalparams) {
        this.iframe.src += '&parentTitle=' + encodeURIComponent(document.title);
        this.iframe.src += '&' + this.settings.parenturlparam + '=' + encodeURIComponent(this.settings.parenturlvalue);
      }
      this.iframe.src += hash;
      this.iframe.setAttribute('width', '100%');
      this.iframe.setAttribute('scrolling', 'no');
      this.iframe.setAttribute('marginheight', '0');
      this.iframe.setAttribute('frameborder', '0');
      if (this.settings.title) {
        this.iframe.setAttribute('title', this.settings.title);
      }
      if (this.settings.allowfullscreen !== undefined && this.settings.allowfullscreen !== false) {
        this.iframe.setAttribute('allowfullscreen', '');
      }
      if (this.settings.sandbox !== undefined && typeof this.settings.sandbox === 'string') {
        this.iframe.setAttribute('sandbox', this.settings.sandbox);
      }
      if (this.settings.id) {
        if (!document.getElementById(this.settings.id)) {
          this.iframe.setAttribute('id', this.settings.id);
        }
      }
      if (this.settings.name) {
        this.iframe.setAttribute('name', this.settings.name);
      }
      while (this.el.firstChild) {
        this.el.removeChild(this.el.firstChild);
      }
      this.el.appendChild(this.iframe);
      window.addEventListener('resize', this._onResize);
      if (this.settings.trackscroll) {
        window.addEventListener('scroll', this._throttleOnScroll);
      }
    };
    this._onResize = function () {
      this.sendWidth();
      if (this.settings.trackscroll) {
        this.sendViewportAndIFramePosition();
      }
    }.bind(this);
    this._onScroll = function () {
      this.sendViewportAndIFramePosition();
    }.bind(this);
    this._fire = function (messageType, message) {
      if (messageType in this.messageHandlers) {
        for (var i = 0; i < this.messageHandlers[messageType].length; i++) {
          this.messageHandlers[messageType][i].call(this, message);
        }
      }
    };
    this.remove = function () {
      window.removeEventListener('message', this._processMessage);
      window.removeEventListener('resize', this._onResize);
      this.el.removeChild(this.iframe);
      _cleanAutoInitInstances();
    };
    this._processMessage = function (e) {
      if (!_isSafeMessage(e, this.settings)) {
        return;
      }
      if (typeof e.data !== 'string') {
        return;
      }
      var match = e.data.match(this.messageRegex);
      if (!match || match.length !== 3) {
        return false;
      }
      var messageType = match[1];
      var message = match[2];
      this._fire(messageType, message);
    }.bind(this);
    this._onHeightMessage = function (message) {
      var height = parseInt(message);
      this.iframe.setAttribute('height', height + 'px');
    };
    this._onNavigateToMessage = function (message) {
      if (!_isSafeUrl(message)) {
        return;
      }
      document.location.href = message;
    };
    this._onScrollToChildPosMessage = function (message) {
      var iframePos = document.getElementById(this.id).getBoundingClientRect().top + window.pageYOffset;
      var totalOffset = iframePos + parseInt(message);
      window.scrollTo(0, totalOffset);
    };
    this.onMessage = function (messageType, callback) {
      if (!(messageType in this.messageHandlers)) {
        this.messageHandlers[messageType] = [];
      }
      this.messageHandlers[messageType].push(callback);
    };
    this.sendMessage = function (messageType, message) {
      if (this.el.getElementsByTagName('iframe').length) {
        if (this.el.getElementsByTagName('iframe')[0].contentWindow) {
          this.el.getElementsByTagName('iframe')[0].contentWindow.postMessage(_makeMessage(this.id, messageType, message), '*');
        } else {
          this.remove();
        }
      }
    };
    this.sendWidth = function () {
      var width = this.el.offsetWidth.toString();
      this.sendMessage('width', width);
    };
    this.sendViewportAndIFramePosition = function () {
      var iframeRect = this.iframe.getBoundingClientRect();
      var vWidth = window.innerWidth || document.documentElement.clientWidth;
      var vHeight = window.innerHeight || document.documentElement.clientHeight;
      var payload = vWidth + ' ' + vHeight;
      payload += ' ' + iframeRect.top + ' ' + iframeRect.left;
      payload += ' ' + iframeRect.bottom + ' ' + iframeRect.right;
      this.sendMessage('viewport-iframe-position', payload);
    };
    for (var key in config) {
      this.settings[key] = config[key];
    }
    this._throttleOnScroll = _throttle(this._onScroll.bind(this), this.settings.scrollwait);
    this.onMessage('height', this._onHeightMessage);
    this.onMessage('navigateTo', this._onNavigateToMessage);
    this.onMessage('scrollToChildPos', this._onScrollToChildPosMessage);
    this.onMessage('parentPositionInfo', this.sendViewportAndIFramePosition);
    window.addEventListener('message', this._processMessage, false);
    this._constructIframe();
    return this;
  };
  lib.Child = function (config) {
    this.parentWidth = null;
    this.id = null;
    this.parentTitle = null;
    this.parentUrl = null;
    this.settings = {
      renderCallback: null,
      xdomain: '*',
      polling: 0,
      parenturlparam: 'parentUrl'
    };
    this.timerId = null;
    this.messageRegex = null;
    this.messageHandlers = {};
    config = config || {};
    this.onMessage = function (messageType, callback) {
      if (!(messageType in this.messageHandlers)) {
        this.messageHandlers[messageType] = [];
      }
      this.messageHandlers[messageType].push(callback);
    };
    this._fire = function (messageType, message) {
      if (messageType in this.messageHandlers) {
        for (var i = 0; i < this.messageHandlers[messageType].length; i++) {
          this.messageHandlers[messageType][i].call(this, message);
        }
      }
    };
    this._processMessage = function (e) {
      if (!_isSafeMessage(e, this.settings)) {
        return;
      }
      if (typeof e.data !== 'string') {
        return;
      }
      var match = e.data.match(this.messageRegex);
      if (!match || match.length !== 3) {
        return;
      }
      var messageType = match[1];
      var message = match[2];
      this._fire(messageType, message);
    }.bind(this);
    this._onWidthMessage = function (message) {
      var width = parseInt(message);
      if (width !== this.parentWidth) {
        this.parentWidth = width;
        if (this.settings.renderCallback) {
          this.settings.renderCallback(width);
        }
        this.sendHeight();
      }
    };
    this.sendMessage = function (messageType, message) {
      window.parent.postMessage(_makeMessage(this.id, messageType, message), '*');
    };
    this.sendHeight = function () {
      var height = document.getElementsByTagName('body')[0].offsetHeight.toString();
      this.sendMessage('height', height);
      return height;
    }.bind(this);
    this.getParentPositionInfo = function () {
      this.sendMessage('parentPositionInfo');
    };
    this.scrollParentTo = function (hash) {
      this.sendMessage('navigateTo', '#' + hash);
    };
    this.navigateParentTo = function (url) {
      this.sendMessage('navigateTo', url);
    };
    this.scrollParentToChildEl = function (id) {
      var topPos = document.getElementById(id).getBoundingClientRect().top + window.pageYOffset;
      this.scrollParentToChildPos(topPos);
    };
    this.scrollParentToChildPos = function (pos) {
      this.sendMessage('scrollToChildPos', pos.toString());
    };
    var _markWhetherEmbedded = function _markWhetherEmbedded(onMarkedEmbeddedStatus) {
      var htmlElement = document.getElementsByTagName('html')[0],
          newClassForHtml,
          originalHtmlClasses = htmlElement.className;
      try {
        if (window.self !== window.top) {
          newClassForHtml = "embedded";
        } else {
          newClassForHtml = "not-embedded";
        }
      } catch (e) {
        newClassForHtml = "embedded";
      }
      if (originalHtmlClasses.indexOf(newClassForHtml) < 0) {
        htmlElement.className = originalHtmlClasses ? originalHtmlClasses + ' ' + newClassForHtml : newClassForHtml;
        if (onMarkedEmbeddedStatus) {
          onMarkedEmbeddedStatus(newClassForHtml);
        }
        _raiseCustomEvent("marked-embedded");
      }
    };
    this.remove = function () {
      window.removeEventListener('message', this._processMessage);
      if (this.timerId) {
        clearInterval(this.timerId);
      }
    };
    for (var key in config) {
      this.settings[key] = config[key];
    }
    this.id = _getParameterByName('childId') || config.id;
    this.messageRegex = new RegExp('^pym' + MESSAGE_DELIMITER + this.id + MESSAGE_DELIMITER + '(\\S+)' + MESSAGE_DELIMITER + '(.*)$');
    var width = parseInt(_getParameterByName('initialWidth'));
    this.parentUrl = _getParameterByName(this.settings.parenturlparam);
    this.parentTitle = _getParameterByName('parentTitle');
    this.onMessage('width', this._onWidthMessage);
    window.addEventListener('message', this._processMessage, false);
    if (this.settings.renderCallback) {
      this.settings.renderCallback(width);
    }
    this.sendHeight();
    if (this.settings.polling) {
      this.timerId = window.setInterval(this.sendHeight, this.settings.polling);
    }
    _markWhetherEmbedded(config.onMarkedEmbeddedStatus);
    return this;
  };
  if (typeof document !== "undefined") {
    lib.autoInit(true);
  }
  return lib;
});

/***/ }),

/***/ 216:
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _pym = __webpack_require__(134);

;
(function () {
  'use strict';

  window.pymChild = new _pym.Child();
  window.addEventListener('load', function () {
    window.pymChild.sendHeight();
    window.pymChild.sendMessage('pdfappready', true);
    var anchors = document.getElementsByTagName('a');
    Array.prototype.slice.call(anchors).forEach(function (el) {
      el.addEventListener('click', function (e) {
        if (this.href !== undefined && this.href !== "" && this.href[0] !== '#') {
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

/***/ })

/******/ });