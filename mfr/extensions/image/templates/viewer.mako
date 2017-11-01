

<img style="max-width: 1200; max-height: 1200;" src="${url}">

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>

<script src="/static/js/jquery-1.11.3.min.js"></script>
<script src="${base}/js/jquery.zoom.min.js"></script>

<script>
$(document).ready(function(){
  $('img')
    .wrap('<span style="display:inline-block"></span>')
    .css('display', 'block')
    .parent()
    .zoom();
});
</script>