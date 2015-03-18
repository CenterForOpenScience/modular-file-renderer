<div id="viewer" style="width: auto; height: 400px; background-color: black;"></div>
<script>
(function () {
    var viewer = pv.Viewer($('#viewer')[0], {
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
