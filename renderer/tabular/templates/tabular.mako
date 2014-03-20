<!-- SlickGrid CSS -->
<link rel="stylesheet" href="/static/tabular/css/slick.grid.css" type="text/css"/>
<link rel="stylesheet" href="/static/tabular/css/jquery-ui-1.8.16.custom.css" type="text/css"/>
<link rel="stylesheet" href="/static/tabular/css/examples.css" type="text/css"/>
<link rel="stylesheet" href="/static/tabular/css/slick-default-theme.css" type="text/css"/>

<!-- SlickGrid JS -->
<script src="/static/tabular/js/jquery-1.7.min.js"></script>
<script src="/static/tabular/js/jquery.event.drag-2.2.js"></script>
<script src="/static/tabular/js/slick.core.js"></script>
<script src="/static/tabular/js/slick.grid.js"></script>
<div>${writing}</div>
<div id="mfrGrid" style="width: 600px; height: 600px;"></div>

<script>
(function(){
    var columns = ${columns};
    var rows = ${rows};

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