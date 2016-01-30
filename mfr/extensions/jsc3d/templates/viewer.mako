<canvas id="mfrViewer"></canvas>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
<script>
    window.pymChild.sendMessage('embed', 'embed-responsive-16by9');
</script>

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

<script type="text/javascript">
  var canvas = document.getElementById('mfrViewer');
  canvas.width  = window.innerWidth * 0.95;
  canvas.height = 500;
  var viewer = new JSC3D.Viewer(canvas);
  viewer.setParameter('SceneUrl', '${url}${ext}');
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
    var _loadFromUrl = loader.loadFromUrl;
    loader.loadFromUrl = _loadFromUrl.bind(loader, '${url}');
    return loader;
  };

  viewer.init();
  viewer.update();
</script>
