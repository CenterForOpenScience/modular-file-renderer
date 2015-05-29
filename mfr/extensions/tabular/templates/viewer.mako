<link rel="stylesheet" href="${base}/css/slick.grid.css">
<link rel="stylesheet" href="${base}/css/slick-default-theme.css">

<div id="mfrGrid" style="width: 100%; height: 100%;"></div>

<script>
    function getScripts(files, callback) {
        $.getScript(files.shift(), function() {
           files.length ? getScripts(files, callback) : callback();
        });
    }

    getScripts([
        '${base}/js/jquery.event.drag-2.2.js',
        '${base}/js/slick.core.js',
        '${base}/js/slick.grid.js'
    ], function () {
        var columns = ${columns};
        var rows = ${rows};
        var options = ${options};
        var grid = new Slick.Grid("#mfrGrid", rows, columns, options);
    });
</script>
