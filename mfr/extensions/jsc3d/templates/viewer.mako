<canvas id="mfrViewer" style="border: 1px solid;"></canvas>
<script src="${base}/js/jsc3d.js"></script>
<script src="${base}/js/jsc3d.touch.js"></script>
<script src="${base}/js/jsc3d.webgl.js"></script>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>

<script>
    window.pymChild.sendMessage('embed', 'embed-responsive-16by9');
</script>

<script type="text/javascript">
  var canvas = document.getElementById('mfrViewer');
  canvas.width  = window.innerWidth * 0.95;
  canvas.height = 500;
  var viewer = new JSC3D.Viewer(canvas);
  viewer.setParameter('SceneUrl', '${url}${fileExt}');
  viewer.setParameter('InitRotationX', 0);
  viewer.setParameter('InitRotationY', 0);
  viewer.setParameter('InitRotationZ', 0);
  viewer.setParameter('ModelColor',       '#CAA618');
  viewer.setParameter('BackgroundColor1', '#FFFFFF');
  viewer.setParameter('BackgroundColor2', '#FFFFFF');
  viewer.setParameter('RenderMode', 'texturesmooth');
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
