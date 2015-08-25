<link rel="stylesheet" href="${base}/css/slick.grid.css">
<link rel="stylesheet" href="${base}/css/slick-default-theme.css">
<link rel="stylesheet" href="${base}/css/examples.css">
<link rel="stylesheet" href="${base}/css/bootstrap.min.css">

<div id="mfrViewer" style="min-height: ${height}px;">
    <nav><ul id="tabular-tabs" class="nav nav-tabs">
    </ul></nav>
    <div id="mfrGrid" style="min-height: ${height}px;">
    </div>
</div>

<script src="/static/js/jquery-1.11.3.min.js"></script>
<script src="${base}/js/bootstrap.min.js"></script>
<script src="${base}/js/jquery.event.drag-2.2.js"></script>
<script src="${base}/js/slick.core.js"></script>
<script src="${base}/js/slick.grid.js"></script>
<script>
    $(function () {
        var sheets = ${sheets};
        var options = ${options};
        var gridArr = {};
        var grid;

        for (var sheetName in sheets){
            var sheet = sheets[sheetName];
            sheetName = sheetName.replace(' ', '_');
            $("#tabular-tabs").append('<li role="presentation"><a id="' + sheetName + '" aria-controls="' + sheetName + '" role="tab" data-toggle="tab">'+ sheetName + '</a></li>');
            gridArr[sheetName] = [sheet[0], sheet[1]];

            $('#'+sheetName).click(function (e) {
                e.preventDefault();
                var columns = gridArr[$(this).attr('id')][0];
                var rows = gridArr[$(this).attr('id')][1];

                grid = new Slick.Grid('#mfrGrid', rows, columns, options);
                grid.onSort.subscribe(function (e, args) {
                    var cols = args.sortCols;
                    rows.sort(function (dataRow1, dataRow2) {
                        for (var i = 0; i < cols.length; i++) {
                            var field = cols[i].sortCol.field;
                            var sign = cols[i].sortAsc ? 1 : -1;
                            var value1 = dataRow1[field], value2 = dataRow2[field];
                            var result = (value1 == value2 ? 0 : (value1 > value2 ? 1 : -1)) * sign;
                            if (result !== 0) {
                                return result;
                            }
                        }
                        return 0;
                    });
                    grid.invalidate();
                    grid.render();
                });
            });
        }

        $("#tabular-tabs").tab();
        $("#tabular-tabs a:first").click();
    });
</script>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
