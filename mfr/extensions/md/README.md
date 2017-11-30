
## Markdown plus Mathjax readme

Most of the packages are in there to try to match what the OSF wiki is doing. The two exceptions being markdown-it-highlightjs.js and markdown-it-mathjax.js. The highlighter matches the functionality of what is on the osf however, and the markdown-it-mathjax.js increases functionality with mathjax. 

to get all the libraries needed:
Note: You do not need to use npm, you can easily get them off of github.

```bash
npm markdown-it@8.4.0
npm install @centerforopenscience/markdown-it-toc@1.1.1
npm install markdown-it-highlightjs@3.0.0
npm install markdown-it-ins-del@0.1.1
npm install markdown-it-sanitizer@0.4.3
npm install markdown-it-mathjax@2.0.0
```

github:

https://github.com/cos-forks/markdown-it-toc
https://github.com/valeriangalliat/markdown-it-highlightjs
https://github.com/brianjgeiger/markdown-it-ins-del
https://github.com/svbergerem/markdown-it-sanitizer
https://github.com/classeur/markdown-it-mathjax

To add a new library, you need to make sure its loadable in md.js somehow, either through exporting via `root.<name>` or some other means. Some of the markdown plugins added have custom code in them to load them into `root`.

Libraries should try to use the same version as the ones used on the OSF. The plugins do not matter as much, but `markdown-it` and `Mathjax` you should try to match exactly because styling can change between versions.

To add a new library that is not already set up to export to `root` can be a bit tricky but the gist of it is, wrap the plugin in this code:

```javascript
;(function (root, factory) {
    if (typeof exports === 'object') {
        module.exports = factory()
  } else {
        root.<PLUGIN_NAME> = factory()
    }
})(this, function () {


    return function(md){

        .....
    }

})
```

And then modify it to work in this context. See other plugins for examples.

Then in md.js, you can add a plugin to the markdown renderer by adding a `.use(window.<PLUGIN_NAME>)` after loading the file into `viewer.mako`.