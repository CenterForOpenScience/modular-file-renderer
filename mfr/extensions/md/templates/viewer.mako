<link href='https://fonts.googleapis.com/css?family=Open+Sans:400,600,300' rel='stylesheet' type='text/css'>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<link type="text/css" rel="stylesheet" href="${base}/css/highlightjs-default.css">
<link rel="stylesheet" href="${base}/css/default.css">

## Quirks:
##
## ``markdownit`` and its plugins take in teh raw MD content and outputs renderable HTML that can be
## directly embedded.  However, for security conerns, MFR mustn't put the raw content onto the page.
## It uses XMLHttpRequest to fetch the file content from WB and let ``markdownit`` santize and parse
## it into the renderable HTML.
##
## Cross Origin Resource Sharing (CORS) is enforced for the XMLHttpRequest.  One one hand, WB has
## already been configured to respond with header "Access-Control-Allow-Origin", which allows the
## MFR domain.  On the other hand, OSF hasn't.  This is why the request must goes to WB directly.
##
<div class="mfrViewer" id="mdViewer"></div>

<script type="text/x-mathjax-config">
    MathJax.Hub.Config({
        tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']], processEscapes: true},
        messageStyle: "none",
        skipStartupTypeset: true
    });
</script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"></script>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>

## Note Loading markdown-it.min.js from CDN does not work
<script src="${base}/js/markdown-it.min.js"></script>
<script src="${base}/js/markdown-it-mathjax.js"></script>
<script src="${base}/js/markdown-it-sanitizer.min.js"></script>
<script src="${base}/js/markdown-it-highlightjs.js"></script>
<script src="${base}/js/markdown-it-ins-del.js"></script>
<script src="${base}/js/markdown-it-toc.js"></script>

<script>

    ## How to load ``markdown-it``: https://github.com/markdown-it/markdown-it#simple
    var MarkdownIt = window.markdownit;

    var bootstrapTable = function(md) {
        md.renderer.rules.table_open = function() { return "<table class=\"table\">"; };
    };

    var markdown = new MarkdownIt("commonmark", {html: true, linkify: true})
        .use(window.markdownitToc)
        .use(window.markdownitIns)
        .use(window.markdownitHightlightjs)
        .use(window.markdownitSanitizer)
        .use(window.markdownitMathjax())
        .enable("table")
        .enable("linkify")
        .use(bootstrapTable)
        .disable("strikethrough");

    var wb_request = new XMLHttpRequest();
    var wb_download_url = "${url}";
    wb_request.open("GET", wb_download_url);
    wb_request.responseType = "text";
    wb_request.withCredentials = true;
    wb_request.onload = function () {
        document.getElementById("mdViewer").innerHTML = markdown.render(wb_request.response);
        ## Force the host to resize
        window.pymChild.sendHeight();
    };
    wb_request.send();
</script>

<script>MathJax.Hub.Queue(["Typeset",MathJax.Hub,"jaxified"]);</script>
