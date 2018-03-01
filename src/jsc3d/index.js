
import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";


debugger;

// Runs when DOM is finished loading.
$(function () {
    $('[data-toggle="popover"]').popover();
    $('#mfrViewer').bind('contextmenu', function () { return false; });
    window.focus();

    var canvas = document.getElementById('mfrViewer');
    canvas.width = window.innerWidth;
    canvas.height = 500;

    var viewer = new JSC3D.Viewer(canvas);
    viewer.setParameter('SceneUrl', window.ext);
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
        loader.loadFromUrl = _loadFromUrl.bind(loader, window.fileUrl);
        return loader;
    };

    viewer.init();
    viewer.update();
});

