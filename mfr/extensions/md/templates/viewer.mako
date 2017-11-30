<link href='https://fonts.googleapis.com/css?family=Open+Sans:400,600,300' rel='stylesheet' type='text/css'>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<link type="text/css" rel="stylesheet" href="${base}/css/highlightjs-default.css">
<link rel="stylesheet" href="${base}/css/default.css">

<div class="mfrViewer" id="jaxified">
    ${body}
</div>

<script type="text/x-mathjax-config">
    MathJax.Hub.Config({
        tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']], processEscapes: true},
        messageStyle: "none",
        skipStartupTypeset: true
    });
</script>

<script type="text/javascript" 
src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"></script>

<!-- Order matters here -->
<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
<script src="${base}/js/markdown-it.min.js"></script>
<script src="${base}/js/markdown-it-mathjax.js"></script>
<script src="${base}/js/markdown-it-sanitizer.min.js"></script>
<script src="${base}/js/markdown-it-highlightjs.js"></script>
<script src="${base}/js/markdown-it-ins-del.js"></script>
<script src="${base}/js/markdown-it-toc.js"></script>
<script src="${base}/js/md.js"></script>

<script> 
    MathJax.Hub.Queue(["Typeset",MathJax.Hub,"jaxified"]);
</script>
