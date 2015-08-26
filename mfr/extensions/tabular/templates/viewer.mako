<link rel="stylesheet" href="${base}/css/slick.grid.css">
<link rel="stylesheet" href="${base}/css/slick-default-theme.css">
<link rel="stylesheet" href="${base}/css/examples.css">
<link rel="stylesheet" href="${base}/css/bootstrap.min.css">

<div id="mfrViewer" style="min-height: ${height}px;">
    <div class="scroller scroller-left"><i class="glyphicon glyphicon-chevron-left"></i></div>
    <div class="scroller scroller-right"><i class="glyphicon glyphicon-chevron-right"></i></div>
    <nav class="wrapper">
        <ul id="tabular-tabs" class="nav nav-tabs list" style="height: 45px; overflow: auto; white-space: nowrap;"> 
        </ul>
    </nav>
    <div id="inlineFilterPanel" style="background:#dddddd;padding:3px;color:black;">
        Show rows with cells including: <input type="text" id="txtSearch">
    </div>
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
        var data;
        var searchString = "";

        for (var sheetName in sheets){
            var sheet = sheets[sheetName];
            sheetName = sheetName.replace( /(:|\.|\[|\]|,|@|&|\ )/g, '_' ); //Handle characters that can't be in DOM ID's
            $("#tabular-tabs").append('<li role="presentation" style="display:inline-block; float: none;"><a id="' + sheetName + '" aria-controls="' + sheetName + '" role="tab" data-toggle="tab">'+ sheetName + '</a></li>');
            gridArr[sheetName] = [sheet[0], sheet[1]];

            $('#'+sheetName).click(function (e) {
                e.preventDefault();
                var columns = gridArr[$(this).attr('id')][0];
                var rows = gridArr[$(this).attr('id')][1];

                grid = new Slick.Grid('#mfrGrid', rows, columns, options);
                searchString = "";
                $("#txtSearch").value = "";
                data = grid.getData();
                grid.onSort.subscribe(sortData);
            });
        }

        $("#tabular-tabs").tab();
        $("#tabular-tabs a:first").click();

        $("#txtSearch").keyup(function (e) {
            // clear on Esc
            if (e.which == 27) {
              this.value = "";
            }
            searchString = this.value;
            var filteredData = (searchString !== "") ? filterData(data, searchString) : data;
            grid = new Slick.Grid('#mfrGrid', filteredData, grid.getColumns(), options);
            grid.onSort.subscribe(sortData);
        });

        $(".list").on('scroll', function (e) {
            reAdjust();
        });

        function filterData(data, search) {
            var filteredData = [];
            for (var i = 0; i<data.length; i++){
                var filtered = false;
                var item = data[i];
                for (var title in item) {
                    if (search !== "" && item[title].toString().indexOf(search) !== -1) {
                        filtered = filtered || true;
                        continue;
                    }
                }
                if (filtered){
                    filteredData.push(item);
                }
            }
            return filteredData;
        }

        function sortData (e, args) {
            var cols = args.sortCols;
            var rows = grid.getData();
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
        }
        
        function reAdjust(){
            liFirst = $('.list li:first');
            liLast = $('.list li:last');
            widthOfList = liLast.position().left - liFirst.position().left;
            console.log('f/l/m :' + liFirst.position().left + '/' + liLast.position().left + '/' + widthOfList);
            if (liFirst.position().left < 0) {
                $('.scroller-left').show();
            }
            else {
                $('.scroller-left').hide();
            }

            if ((liLast.position().left + liLast.width()) < (widthOfList-10)) {
                $('.scroller-right').hide();
            }
            else {
                $('.scroller-right').show();
            }
        }

        reAdjust();
    });
</script>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
