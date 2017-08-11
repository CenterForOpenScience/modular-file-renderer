<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,600,300,700" rel="stylesheet" type="text/css">
<link type="text/css" rel="stylesheet" href="/static/css/default.css">
<link type="text/css" rel="stylesheet" href="/static/css/highlightjs-default.css">

<script type="text/x-mathjax-config">
    MathJax.Hub.Config({
        tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']], processEscapes: true},
        // Don't automatically typeset the whole page. Must explicitly use MathJax.Hub.Typeset
        messageStyle: "none",
        skipStartupTypeset: true
    });
</script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS_CHTML"></script>

<div style="word-wrap: break-word;" class="mfrViewer" id="jaxified">
${body}
</div>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
<script src="/static/js/mdbundle.js"></script>

<script> 
    MathJax.Hub.Queue(["Typeset",MathJax.Hub,"jaxified"]);
</script>
