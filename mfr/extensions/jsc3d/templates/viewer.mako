<link rel="stylesheet" href="/static/css/bootstrap.min.css">
<style type="text/css">
    .popover {
        max-width: 100%;
    }
</style>
<script src="/static/js/jquery-1.11.3.min.js" type="text/javascript"></script>
<script src="/static/js/bootstrap.min.js" type="text/javascript"></script>

<canvas id="mfrViewer" tabindex="-1"></canvas>
<a style="position: absolute; top: 10px; right: 10px; cursor: pointer;"
   data-toggle="popover" data-trigger="hover" data-placement="left" data-html="true"
   data-content="Drag mouse to rotate<br>Drag mouse with ctrl pressed to pan<br>Drag mouse with shift pressed to zoom">
   <img src="${base}/images/question-circle.png">
</a>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>

<!--[if !IE]><!-->
<script type="text/javascript" src="${base}/js/jsc3d.js"></script>
<!--<![endif]-->
<!--[if IE]>
<script type="text/javascript" src="${base}/js/jsc3d_ie.js"></script>
<script type="text/javascript">
  JSC3D.Texture.cv = document.getElementById('mfrViewer');
</script>
<![endif]-->
<script src="${base}/js/jsc3d.touch.js"></script>
<script src="${base}/js/jsc3d.webgl.js"></script>

% if ext in ['.3ds']:
<script src="${base}/js/jsc3d.3ds.js"></script>
% elif ext in ['.ctm']:
<script src="${base}/js/jsc3d.ctm.js"></script>
% endif

<script>
    $(function () {
        $('[data-toggle="popover"]').popover();
        $('#mfrViewer').bind('contextmenu', function () { return false; });
        window.focus();

        var canvas = document.getElementById('mfrViewer');
        canvas.width = window.innerWidth;
        canvas.height = 500;

        var viewer = new JSC3D.Viewer(canvas);
        viewer.setParameter('SceneUrl', '${ext}');
        viewer.setParameter('InitRotationX', -15);
        viewer.setParameter('InitRotationY', 0);
        viewer.setParameter('InitRotationZ', 0);
        viewer.setParameter('ModelColor', '#CCCCCC');
        viewer.setParameter('BackgroundColor1', '#FFFFFF');
        viewer.setParameter('BackgroundColor2', '#FFFFFF');
        viewer.setParameter('RenderMode', 'textureflat');
        viewer.setParameter('MipMapping', 'on');
        viewer.setParameter('Renderer', 'webgl');
        viewer.setParameter('Definition', 'high');

        var _getLoader = JSC3D.LoaderSelector.getLoader;
        JSC3D.LoaderSelector.getLoader = function (fileExtName) {
            var loader = _getLoader(fileExtName);
            if (!loader) {
                return viewer.reportProgress('Unable to load renderer for file of type \'' + fileExtName + '\'', 0);
            }
            var _loadFromUrl = loader.loadFromUrl;
            loader.loadFromUrl = _loadFromUrl.bind(loader, '${url}');
            return loader;
        };

        viewer.init();
        viewer.update();
   });
</script>
