<style type="text/css">
    .popover {
        max-width: 100%;
    }
</style>

<script>
    window.fileUrl = '${url}';
    window.ext = '${ext}';
</script>

<canvas id="mfrViewer" tabindex="-1"></canvas>
<a style="position: absolute; top: 10px; right: 10px; cursor: pointer;"
   data-toggle="popover" data-trigger="hover" data-placement="left" data-html="true"
   data-content="<p><b> Rotate:</b> Click and drag</p>
                 <p><b> Pan:</b> Ctrl + click and drag</p>
                 <p><b> Zoom:</b> Shift + click and drag up/down</p>">
   <img src="/assets/question-circle.png">
</a>

<script src="/assets/jsc3d-init.js"></script>

<script src="/assets/mfr.child.js"></script>

<!--[if !IE]><!-->
<script type="text/javascript" src="/assets/jsc3d.js"></script>
<!--<![endif]-->
<!--[if IE]>
<script type="text/javascript" src="/assets/jsc3d_ie.js"></script>
<script type="text/javascript">
  JSC3D.Texture.cv = document.getElementById('mfrViewer');
</script>
<![endif]-->
<script src="/assets/jsc3d.touch.js"></script>
<script src="/assets/jsc3d.webgl.js"></script>

% if ext in ['.3ds']:
<script src="/assets/jsc3d.3ds.js"></script>
% elif ext in ['.ctm']:
<script src="/assets/jsc3d.ctm.js"></script>
% endif

<script>
    console.log("FIRST");
</script>


