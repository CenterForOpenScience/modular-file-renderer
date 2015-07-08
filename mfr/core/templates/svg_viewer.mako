<%inherit file="extras.mako"/>
<img class="mfrViewer" data-src="${url}">

<script>
    (function () {
        $(function () {
            $.getScript('${base}/js/svg-injector.min.js',
                function () {
                    var mySVGsToInject = document.querySelectorAll('img.mfrViewer');
                    SVGInjector(mySVGsToInject);
                }
            );
        });
    })();
</script>
