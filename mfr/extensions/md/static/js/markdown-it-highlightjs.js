/**
 * Preset to use highlight.js with markdown-it.
 *
 * Origin: https://github.com/valeriangalliat/markdown-it-highlightjs/tree/v3.0.0/index.js
 *  The above link gives a 404. Here is a forked copy and Babel-converted ES5 version:
 *  (ES6) https://github.com/cslzchen/markdown-it-highlightjs/blob/release/3.0.0/index.js
 *  (ES5) https://github.com/cslzchen/markdown-it-highlightjs/blob/release/3.0.0/index.es5.js
 *
 * Version: https://github.com/valeriangalliat/markdown-it-highlightjs/releases/tag/v3.0.0
 */

(function (root, factory) {
    if (typeof exports === "object") {
        module.exports = factory();
    } else {
        root.markdownitHightlightjs = factory();
    }
})(this, function () {

    "use strict";

    var maybe = function maybe(f) {
        try {
            return f();
        } catch (e) {
            return false;
        }
    };

    // Highlight with given language.
    var highlight = function highlight(code, lang) {
        return maybe(function () {
            return hljs.highlight(lang, code, true).value;
        }) || "";
    };

    // Highlight with given language or automatically.
    var highlightAuto = function highlightAuto(code, lang) {
        return lang ? highlight(code, lang) : maybe(function () {
            return hljs.highlightAuto(code).value;
        }) || "";
    };

    // Wrap a render function to add `hljs` class to code blocks.
    var wrap = function wrap(render) {
        return function () {
            for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
                args[_key] = arguments[_key];
            }

            return render.apply(this, args).replace("<code class=\"", "<code class=\"hljs ").replace("<code>", "<code class=\"hljs\">");
        };
    };

    var defaults = {
        auto: true,
        code: true
    };

    return function(md, opts) {

        opts = Object.assign({}, defaults, opts);

        md.options.highlight = opts.auto ? highlightAuto : highlight;
        md.renderer.rules.fence = wrap(md.renderer.rules.fence);

        if (opts.code) {
            md.renderer.rules.code_block = wrap(md.renderer.rules.code_block);
        }
    };

});
