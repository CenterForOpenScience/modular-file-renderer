<div>${writing}</div>
<div id="mfrGrid" style="width: ${width}px; height: ${height}px;"></div>

<script>
(function(){
    var columns = ${columns};
    var rows = ${rows};

## TODO(asmacdo)
##todo make this based on the size of the window instead of hardcoded in -ajs
    if(columns.length < 9){
        var options = {
            enableCellNavigation: true,
            enableColumnReorder: false,
            forceFitColumns: true,
            syncColumnCellResize: true
        };
        }else{
        var options = {
            enableCellNavigation: true,
            enableColumnReorder: false,
            syncColumnCellResize: true
        };
    }

    var grid = new Slick.Grid("#mfrGrid", rows, columns, options);
})();
</script>
