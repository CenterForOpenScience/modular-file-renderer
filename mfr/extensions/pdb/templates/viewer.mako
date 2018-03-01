<div id="mfrViewer"></div>

<script src="/assets/mfr.child.js"></script>
<script>
    window.pymChild.sendMessage('embed', 'embed-responsive-16by9');
</script>

<script src="/assets/jquery-1.11.3.min.js"></script>
<script src="/assets/gl-matrix.js"></script>
<script src="/assets/core.js"></script>
<script src="/assets/geom.js"></script>
<script src="/assets/trace.js"></script>
<script src="/assets/symmetry.js"></script>
<script src="/assets/mol.js"></script>
<script src="/assets/io.js"></script>
<script src="/assets/vert-assoc.js"></script>
<script src="/assets/buffer-allocators.js"></script>
<script src="/assets/vertex-array-base.js"></script>
<script src="/assets/indexed-vertex-array.js"></script>
<script src="/assets/vertex-array.js"></script>
<script src="/assets/chain-data.js"></script>
<script src="/assets/geom-builders.js"></script>
<script src="/assets/scene.js"></script>
<script src="/assets/render.js"></script>
<script src="/assets/shade.js"></script>
<script src="/assets/cam.js"></script>
<script src="/assets/shaders.js"></script>
<script src="/assets/framebuffer.js"></script>
<script src="/assets/slab.js"></script>
<script src="/assets/animation.js"></script>
<script src="/assets/viewer.js"></script>
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
            async: true,
            url: '${url.replace("'", "\\'")}',
            xhrFields: { withCredentials: true },
        }).done(render);
   })();
</script>
