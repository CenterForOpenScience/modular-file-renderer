<script>
    sheets = ${sheets}
    options = ${options}
</script>

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

<script src="/assets/tabular.js"></script>
