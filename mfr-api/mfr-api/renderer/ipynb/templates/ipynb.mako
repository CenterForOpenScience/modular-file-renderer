<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>${file_name}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- <link href="/static/ipynb/css/ipython.min.css" rel="stylesheet"> -->
    <link href="/static/ipynb/css/pygments.css" rel="stylesheet">
    <link href="/static/ipynb/css/style.min.css" rel="stylesheet">

    <style type="text/css" media='screen and (min-width:980px)'>
        body{
            padding: 50px 100px;
        }
    </style>
    <style type="text/css">
        .imgwrap {
            text-align: center;
        }
        .input_area {
            padding: 0.4em;
        }
        div.input_area > div.highlight > pre {
            margin: 0px;
            padding: 0px;
            border: none;
        }
    </style>

##    ${ if css_theme }
    <link href="/static/ipynb/css/theme/${css_theme}.css" rel="stylesheet">
##    ${ endif }

    <script src="https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"type="text/javascript">
    </script>

    <script type="text/javascript">
    init_mathjax = function() {
        if (window.MathJax) {
            // MathJax loaded
            MathJax.Hub.Config({
                tex2jax: {
                    inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                    displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
                },
                displayAlign: 'left', // Change this to 'center' to center equations.
                "HTML-CSS": {
                    styles: {'.MathJax_Display': {"margin": 0}}
                }
            });
            MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        }
    }
    init_mathjax();
    </script>
  </head>

  <body>
    ${ body | safe}
  </body>
</html>


