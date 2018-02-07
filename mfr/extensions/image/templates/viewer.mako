<script src="/static/js/jquery-1.11.3.min.js"></script>

<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css"/>
<script src="/static/js/bootstrap.min.js"></script>

<div id="msg-heading" class="alert alert-info" role="alert" style="display: none">
    <span data-toggle="collapse" data-trigger="hover" data-target="#msg-content">
        <img src="${base}/images/question-circle.png">
    </span>
    <ul id="msg-content" class="collapse">
        <li>Click on the image to enable zoom and scroll to zoom further</li>
        <li>To view the image in its original size and format, please download.</li>
    </ul>
</div>

<img style="max-width: 100%;" class='baseImage' src="${url}">

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
<script src="/static/js/jquery-1.11.3.min.js"></script>
<script src="${base}/js/jquery.detectmobile.js"></script>
<script src="${base}/js/jquery.mousewheel.min.js"></script>
<script src="${base}/js/jquery.zoom.js"></script>

<script>

    "use strict";

    var magScale = 1;
    var magStep = 0.1;
    var maxScale = 3;
    var minScale = 1;

    var magHeight = null;
    var magWidth = null;

    var heightLimit = null;
    var widthLimit = null;

    // Images with a height less than 150 fails to render correctly when zoom is enabled.
    var heightThreshold = 150;

    var wrapped = false;

    // Enable zoom only for non-mobile browsers
    if (!$.browser.mobile) {

        var is_chrome = !!window.chrome;

        var message = $("#msg-heading");
        message.css({
            "font-size": "12px",
            "padding": "5px 5px 5px 5px",
            "cursor": "pointer;"
        });

        $(document).ready(function() {

            var baseImage = $('.baseImage');

            var addSpan = function() {

                if (!wrapped) {

                    var baseImageHeight = parseInt(baseImage.css('height'));
                    var baseImageWidth = parseInt(baseImage.css('width'));

                    if (heightLimit === baseImageHeight || widthLimit === baseImageWidth) {
                        baseImage.wrap("<div></div>").parent().css({
                            "display": "block",
                            "position": "relative",
                            "overflow": "hidden"
                        });
                        baseImage.parent().wrap("<span></span>").parent().css("display", "inline-block");
                    } else if (!is_chrome) {
                        baseImage.wrap("<div></div>").parent().css("display", "inline-block");
                    } else {
                        baseImage.wrap("<p></p>");
                    }

                    wrapped = true;
                }
            };

            var mouseZoom = function(event, delta) {

                // Disable page scrolling to enable image zooming by mouse scrolling
                event.preventDefault();

                if (delta > 0) {
                    magScale += magStep;
                    magScale = magScale > maxScale ? maxScale : magScale
                } else {
                    magScale -= magStep;
                    magScale = magScale < minScale ? minScale : magScale
                }

                var image = $('.zoomImage');
                magHeight = magHeight === null ? parseInt(image.css('height')) : magHeight;
                magWidth = magWidth === null ? parseInt(image.css('width')) : magWidth;

                image.css({
                    width: magWidth * magScale,
                    height: magHeight * magScale
                });
            };

            $("<img/>").attr("src", $(baseImage[0]).attr("src")).load(function() {
                widthLimit = this.width;
                heightLimit = this.height;

                // Enable zoom only for images with a height of at least 150
                if (heightLimit >= heightThreshold) {
                    $(window).resize(addSpan);
                    var message = $("#msg-heading");
                    message.css("display", "inline-block");
                    addSpan();
                    baseImage.parent().zoom({magnify: magScale}).on('mousewheel', mouseZoom);
                }
            });
        });
    }
</script>
