<script src="http://code.jquery.com/jquery-2.1.4.min.js"></script>
<script src='${base}/js/modernizr.js'></script>
<script src='${base}/js/foundation-5.4.7.min.js'></script>
<script src='${base}/js/gl-matrix.js'></script>
<script src='${base}/js/core.js'></script>
<script src='${base}/js/geom.js'></script>
<script src='${base}/js/trace.js'></script>
<script src='${base}/js/symmetry.js'></script>
<script src='${base}/js/mol.js'></script>
<script src='${base}/js/io.js'></script>
<script src='${base}/js/vert-assoc.js'></script>
<script src='${base}/js/buffer-allocators.js'></script>
<script src='${base}/js/vertex-array-base.js'></script>
<script src='${base}/js/indexed-vertex-array.js'></script>
<script src='${base}/js/chain-data.js'></script>
<script src='${base}/js/geom-builders.js'></script>
<script src='${base}/js/scene.js'></script>
<script src='${base}/js/render.js'></script>
<script src='${base}/js/shade.js'></script>
<script src='${base}/js/cam.js'></script>
<script src='${base}/js/shaders.js'></script>
<script src='${base}/js/framebuffer.js'></script>
<script src='${base}/js/slab.js'></script>
<script src='${base}/js/animation.js'></script>
<script src='${base}/js/viewer.js'></script>

<link rel="stylesheet" href="${base}/css/foundation.css">
<link rel="stylesheet" href="${base}/css/jquery-ui.min.css">
<link rel="stylesheet" href="${base}/css/quint.css">

<div id="mfrViewer" style="width: auto; height: 400px; background-color: black;"></div>
<script>
(function () {
    var viewer = pv.Viewer($('#mfrViewer')[0], {
        width: 'auto',
        height: '400',
        antialias: false,
        outline: true,
        quality: 'medium',
        fog: false
    });

    function render(data) {
        var structure = io.pdb(data);

        viewer.clear();
        viewer.cartoon('structure', structure, {
            color: color.ssSuccession(),
            showRelated: '1'
        });
        viewer.autoZoom();
    }

    function fetch(url) {
        return $.ajax({
            url: url,
            async: true
        }).done(render);
    }

    $(function () {
        var url = '${url.replace("'", "\\'")}';

        $.ajax({
            type: 'HEAD',
            async: true,
            url: url
        }).done(function (message,text,response) {
            return fetch(response.getResponseHeader('Location'));
        }).fail(function () {
            return fetch(url);
        });
    });
})();
</script>
