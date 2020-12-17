## Using Markdown-it with plugins

If we had `npm`, here were the would-be configuration.

```bash
npm markdown-it@8.4.0
npm install @centerforopenscience/markdown-it-toc@1.1.1
npm install markdown-it-highlightjs@3.0.0
npm install markdown-it-ins-del@0.1.1
npm install markdown-it-sanitizer@0.4.3
npm install markdown-it-mathjax@2.0.0
```

For MFR, a customized local copy of each script is stored in the extension's static folder. There are a few issues:

* MFR scripts run directly in the browser without Babel. For ES5 compatibility, developers must use [Babel](https://babeljs.io/repl/) to convert ES6 `markdown-it-highlightjs` to an ES5 version.

* MFR does not use a package manager. Thus, `require` is **NOT** available. For the `viewer.mako` to be able to load these libraries, customization is necessary to export via `root.<PLUGIN_NAME>`. The main script in the `viewer.mako` uses `window.<PLUGIN_NAME>` to access them. `markdown-it` and `markdown-it-sanitizer` are already set up to be exported code. MFR loads the `min` version directly. `markdown-it-toc`, `markdown-it-highlightjs`, `markdown-it-ins-del` and `markdown-it-mathjax` are not. The following wrapper must be used.

    ```javascript
    (function (root, factory) {
        if (typeof exports === "object") {
            module.exports = factory();
        } else {
            root.<PLUGIN_NAME> = factory();
        }
    })  (this, function () {
        return function(md/*, optional arguments*/) {
            /* library code */
        }
    });
    ```

Here is a list of the original copies of the scripts:

* [markdown-it@08.4.0](https://github.com/markdown-it/markdown-it/blob/8.4.0/bin/markdown-it.js)
* [markdown-it-sanitizer@0.4.3](https://github.com/svbergerem/markdown-it-sanitizer/blob/v0.4.3/dist/markdown-it-sanitizer.min.js)
* [markdown-it-mathjax@2.0.0](https://github.com/classeur/markdown-it-mathjax/blob/v2.0.0/markdown-it-mathjax.js)
* [markdown-it-toc@1.1.1](https://github.com/cos-forks/markdown-it-toc/blob/1.1.1/index.js)
* [markdown-it-ins-del@1.0.0](https://github.com/brianjgeiger/markdown-it-ins-del/blob/1.0.0/index.js)
* [markdown-it-higlightjs@3.0.0](https://github.com/cslzchen/markdown-it-highlightjs/blob/release/3.0.0/index.es5.js)
