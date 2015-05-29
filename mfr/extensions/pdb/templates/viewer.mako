<style>
    #mfrViewer > canvas {
      width: 100%;
      height: auto;
    }
</style>

<div id="mfrViewer"></div>

<script>
    (function () {
        function getScripts(files, callback) {
            $.getScript(files.shift(), function () {
                files.length ? getScripts(files, callback) : callback();
            });
        }

        $(function () {
            getScripts([
                '${base}/js/gl-matrix.js',
                '${base}/js/core.js',
                '${base}/js/geom.js',
                '${base}/js/trace.js',
                '${base}/js/symmetry.js',
                '${base}/js/mol.js',
                '${base}/js/io.js',
                '${base}/js/vert-assoc.js',
                '${base}/js/buffer-allocators.js',
                '${base}/js/vertex-array-base.js',
                '${base}/js/indexed-vertex-array.js',
                '${base}/js/vertex-array.js',
                '${base}/js/chain-data.js',
                '${base}/js/geom-builders.js',
                '${base}/js/scene.js',
                '${base}/js/render.js',
                '${base}/js/shade.js',
                '${base}/js/cam.js',
                '${base}/js/shaders.js',
                '${base}/js/framebuffer.js',
                '${base}/js/slab.js',
                '${base}/js/animation.js',
                '${base}/js/viewer.js'
            ], function () {
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

                function fetch(url) {
                    return $.ajax({
                        url: url,
                        async: true
                    }).done(render);
                }

                var url = '${url.replace("'", "\\'")}';
                $.ajax({
                    type: 'HEAD',
                    async: true,
                    url: url
                }).done(function (message, text, response) {
                    return fetch(response.getResponseHeader('Location'));
                }).fail(function () {
                    return fetch(url);
                });
            });
        });
    })();
</script>
