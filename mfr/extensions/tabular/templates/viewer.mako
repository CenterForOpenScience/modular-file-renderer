<link rel="stylesheet" href="${base}/css/slick.grid.css">
<link rel="stylesheet" href="${base}/css/slick-default-theme.css">
<link rel="stylesheet" href="${base}/css/examples.css">

<div id="mfrViewer" style="min-height: ${height}px;"></div>

<script src="/static/js/jquery-1.11.3.min.js"></script>
<script src="${base}/js/jquery.event.drag-2.2.js"></script>
<script src="${base}/js/slick.core.js"></script>
<script src="${base}/js/slick.grid.js"></script>
<script>
    $(function () {
        var columns = ${columns};
        var rows = ${rows};
        var options = ${options};
        new Slick.Grid("#mfrViewer", rows, columns, options);
    });
</script>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
