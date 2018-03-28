<link rel="stylesheet" href="static/css/default.css">
<link rel="stylesheet" href="${base}/jstree-theme/style.css"/>

<script src="/static/js/jquery-1.11.3.min.js"></script>
<script src="/static/js/bootstrap.min.js"></script>

<script src="${base}/js/jstree.min.js"></script>
<script src="${base}/js/jstreetable.js"></script>

<div style="height: 500px;" class="mfrViewer">
    <input id="ziptree_search" class="form-control" style="margin-bottom: 10px;" type="text"  placeholder="Search...">
    <div id="ziptree"></div>
</div>

<script>
    $('#ziptree').jstree({
        "core" : {
            "data" : ${data},
        },
        "plugins" : [
            "table",
            "search"
        ],
        'table': {
		    'columns': [
		        {'header': "Name", 'width': '100%'}, // these widths are strange but work.
                {'header': "Size", 'width': 80, 'value': "size"},
                {'header': "Date", 'width': 150, 'value': "date"}
            ],
        }
    });
    var to = false;
    $('#ziptree_search').keyup(function () {
        if(to) { clearTimeout(to); }
        to = setTimeout(function () {
            var v = $('#ziptree_search').val();
            $('#ziptree').jstree(true).search(v);
        }, 250);
    });
</script>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
