<div id="viewer"></div>
<script>
    (function () {
        function render(url) {
            $('#viewer').html(
                '<iframe src="${base}/web/viewer.html?file=' + encodeURIComponent(url) + '" width="100%" height="600px"></iframe>'
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
