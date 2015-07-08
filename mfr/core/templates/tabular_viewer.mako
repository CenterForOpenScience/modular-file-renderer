<%inherit file="extras.mako"/>
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
        var grid = new Slick.Grid("#mfrViewer", rows, columns, options);
        grid.onSort.subscribe(function (e, args) {
            var cols = args.sortCols;
            rows.sort(function (dataRow1, dataRow2) {
                for (var i = 0; i < cols.length; i++) {
                    var field = cols[i].sortCol.field;
                    var sign = cols[i].sortAsc ? 1 : -1;
                    var value1 = dataRow1[field], value2 = dataRow2[field];
                    var result = (value1 == value2 ? 0 : (value1 > value2 ? 1 : -1)) * sign;
                    if (result != 0) {
                        return result;
                    }
                }
                return 0;
            });
            grid.invalidate();
            grid.render();
        });
    });
</script>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
