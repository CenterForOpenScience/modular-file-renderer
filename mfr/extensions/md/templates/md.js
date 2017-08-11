/* This file is not run, but is used to build static/js/mdbundle.js which is then served in viewer.mako
You need browserify to build the bundle. In order to build it, you need to npm install the proper packages.

npm install -g browserify
npm install markdown-it
npm install @centerforopenscience/markdown-it-toc
npm install markdown-it-highlightjs
npm install markdown-it-ins-del
npm install markdown-it-sanitizer
npm install markdown-it-mathjax

Once all these are installed, invoke this command from the top level directory

//browserify mfr/extensions/md/templates/md.js -o mfr/server/static/js/mdbundle.js
This will build the bundle. viewer.mako will automattically use the new file if it in the right directory

*/


var MarkdownIt = require('markdown-it');

var bootstrapTable = function(md) {
    md.renderer.rules.table_open = function() { return '<table class="table">'; };
};

var markdown = new MarkdownIt('commonmark', {
    html: false, 
})
    // .use(require('markdown-it-video'))
    .use(require('@centerforopenscience/markdown-it-toc'))
    .use(require('markdown-it-sanitizer'))
    .use(require('markdown-it-ins-del'))
    .enable('table')
    .use(bootstrapTable)
    .use(require('markdown-it-highlightjs'), {auto: true, code: true})
    .use(require('markdown-it-mathjax')())
    .disable('strikethrough');

document.getElementById("jaxified").innerHTML = markdown.render(document.getElementById("jaxified").innerHTML)
