<%inherit file="extras.mako"/>
<div id="mfrViewer"></div>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
<script>
    window.pymChild.sendMessage('embed', 'embed-responsive-16by9');
</script>

<script src="/static/js/jquery-1.11.3.min.js"></script>
<script src="${base}/js/gl-matrix.js"></script>
<script src="${base}/js/core.js"></script>
<script src="${base}/js/geom.js"></script>
<script src="${base}/js/trace.js"></script>
<script src="${base}/js/symmetry.js"></script>
<script src="${base}/js/mol.js"></script>
<script src="${base}/js/io.js"></script>
<script src="${base}/js/vert-assoc.js"></script>
<script src="${base}/js/buffer-allocators.js"></script>
<script src="${base}/js/vertex-array-base.js"></script>
<script src="${base}/js/indexed-vertex-array.js"></script>
<script src="${base}/js/vertex-array.js"></script>
<script src="${base}/js/chain-data.js"></script>
<script src="${base}/js/geom-builders.js"></script>
<script src="${base}/js/scene.js"></script>
<script src="${base}/js/render.js"></script>
<script src="${base}/js/shade.js"></script>
<script src="${base}/js/cam.js"></script>
<script src="${base}/js/shaders.js"></script>
<script src="${base}/js/framebuffer.js"></script>
<script src="${base}/js/slab.js"></script>
<script src="${base}/js/animation.js"></script>
<script src="${base}/js/viewer.js"></script>
<script>
    (function () {
        var viewer = pv.Viewer($('#mfrViewer')[0], ${options});

        function render(data) {
            var structure = io.pdb(data);

            viewer.clear();
            viewer.cartoon('structure', structure, {
                color: color.ssSuccession(),
                showRelated: '1'
            });
            viewer.autoZoom();
        }

        $.ajax({
            url: '${url.replace("'", "\\'")}',
            async: true
        }).done(render);
   })();
</script>
