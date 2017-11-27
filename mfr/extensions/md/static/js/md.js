var MarkdownIt = window.markdownit;

var bootstrapTable = function(md) {
    md.renderer.rules.table_open = function() { return '<table class="table">'; };
};

var markdown = new MarkdownIt('commonmark', {
    html: false,
    linkify: true
})
    .use(window.markdownitToc)
    .use(window.markdownitIns)
    .use(window.markdownitHightlightjs)
    .use(window.markdownitSanitizer)
    .use(window.markdownitMathjax())
    .enable('table')
    .enable('linkify')
    .use(bootstrapTable)
    .disable('strikethrough');

document.getElementById("jaxified").innerHTML = markdown.render(document.getElementById("jaxified").innerHTML)
