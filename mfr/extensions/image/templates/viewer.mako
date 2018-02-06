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

    var inLined = false;

    // Enable zoom only for non-mobile browsers
    if (!$.browser.mobile) {

        $(document).ready(function() {

            var baseImage = $('.baseImage');

            var addSpan = function() {

                if (!inLined) {

                    var baseImageHeight = parseInt(baseImage.css('height'));
                    var baseImageWidth = parseInt(baseImage.css('width'));

                    console.log('base = (' + baseImageHeight + ', ' + baseImageWidth + ')');
                    console.log('limit = (' + heightLimit + ', ' + widthLimit + ')');

                    if (heightLimit === baseImageHeight || widthLimit === baseImageWidth) {
                        baseImage
                                .parent()
                                .wrap('<span style="display:inline-block"></span>')
                                .css('display', 'inline-block');
                    } else {
                        baseImage.parent().css('display', 'inline-block');
                    }
                    inLined = true;
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

                console.log('magification scale = ' + magScale);

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
                    addSpan();
                    baseImage.parent().zoom({magnify: magScale}).on('mousewheel', mouseZoom);
                }
            });
        });
    }
</script>
