<link rel="stylesheet" href="${base}/css/ipynb.css">
<link rel="stylesheet" href="${base}/css/pygments.css">

<div class="mfr-ipynb-body">
${body | n}
</div>

<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>
<script type="text/x-mathjax-config">
    config = MathJax.Hub.Config();
    MathJax.Hub.Config({
        extensions: ["tex2jax.js"],
        jax: ["input/TeX", "output/HTML-CSS"],
        tex2jax: {
            inlineMath: [ ['$','$'], ["\\(","\\)"] ],
            displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
            processEscapes: true,
            processEnvironments: true
        },
        // Center justify equations in code and markdown cells. Elsewhere
        // we use CSS to left justify single line equations in code cells.
        displayAlign: 'center',
        "HTML-CSS": {
            styles: {'.MathJax_Display': {"margin": 0}},
            linebreaks: { automatic: true }
        },
	    // Nonn-processing options
	    showProcessingMessages: false,
	    showMathMenu: false,
	    showMathMenuMSIE: false
    });
</script>