<div id="mfrViewer" class="embed-responsive" style="padding-bottom: 95%; border-bottom: solid 1px #404040;">
    <iframe class="embed-responsive-item" src="${base}/web/viewer.html?file=${url}" frameborder="0" allowfullscreen webkitallowfullscreen></iframe>
</div>

##<script>
##    (function () {
##        function render(url) {
##            $('#mfrViewer').html(
##                '<iframe class="embed-responsive-item" src="${base}/web/viewer.html?file=' + encodeURIComponent(url) + '" frameborder="0" allowfullscreen webkitallowfullscreen></iframe>'
##            );
##        }
##
##        $(function () {
##            var url = '${url.replace("'", "\\'")}';
##
##            $.ajax({
##                type: 'HEAD',
##                async: true,
##                url: url
##            }).done(function (message,text,response) {
##                return render(response.getResponseHeader('Location'));
##            }).fail(function () {
##                return render(url);
##            });
##        });
##    })();
##</script>
