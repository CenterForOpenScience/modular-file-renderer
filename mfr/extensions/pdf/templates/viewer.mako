<script src="http://code.jquery.com/jquery-2.1.4.min.js"></script>

<div id="mfrViewer" class="embed-responsive" style="padding-bottom: 95%; border-bottom: solid 1px #404040;"></div>
<script>
    (function () {
        function render(url) {
            $('#mfrViewer').html(
                '<iframe class="embed-responsive-item" src="${base}/web/viewer.html?file=' + encodeURIComponent(url) + '" frameborder="0" allowfullscreen webkitallowfullscreen></iframe>'
            );
        }

        $(function () {
            var url = '${url.replace("'", "\\'")}';

            $.ajax({
                type: 'HEAD',
                async: true,
                url: url
            }).done(function (message,text,response) {
                return render(response.getResponseHeader('Location'));
            }).fail(function () {
                return render(url);
            });
        });
    })();
</script>