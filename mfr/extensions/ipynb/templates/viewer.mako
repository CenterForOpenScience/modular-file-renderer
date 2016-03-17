<link rel="stylesheet" href="${base}/css/ipynb.css">
<link rel="stylesheet" href="${base}/css/pygments.css">
<link rel="stylesheet" href="/static/css/default.css">


<div style="word-wrap: break-word;" class="mfrViewer mfr-ipynb-body">
    ${body | n}
</div>

<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>
<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
<script>
    (function () {
        MathJax.Hub.Config({
            extensions: ["tex2jax.js"],
            jax: ["input/TeX", "output/HTML-CSS"],
            tex2jax: {
                inlineMath: [['$', '$'], ["\\(", "\\)"]],
                displayMath: [['$$', '$$'], ["\\[", "\\]"]],
                processEscapes: true,
                processEnvironments: true
            },
            // Center justify equations in code and markdown cells. Elsewhere
            // we use CSS to left justify single line equations in code cells.
            displayAlign: 'center',
            "HTML-CSS": {
                styles: {'.MathJax_Display': {"margin": 0}},
                linebreaks: {automatic: true}
            },
            // Nonn-processing options
            showProcessingMessages: false,
            showMathMenu: false,
            showMathMenuMSIE: false
        });
    })();
</script>
