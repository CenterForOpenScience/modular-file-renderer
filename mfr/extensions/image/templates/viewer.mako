<script src="/static/js/jquery-1.11.3.min.js"></script>

<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css"/>
<script src="/static/js/bootstrap.min.js"></script>

## Quirks 0:
##
## Need to add this block buffer so that the question circle does not overlap with the image. The
## height will be set if zoom feature is enabled for the give image. The height is set to be 38px,
## which includes 10px each for top and bottom margin, and 18px for the question circle icon.
##
<div id="popover-buffer" style="display: none"></div>
<a id="popover-content" style="display: none" data-toggle="popover"
   data-trigger="hover" data-placement="left" data-html="true"
   data-content="
    <p><b> HiRes:</b> Click on the image to view in higher resolution when available</p>
    <p><b> Zoom:</b> Click on the image and use the mouse wheel to zoom in and out</p>
    <p><b> Navigate:</b> Move the mouse cursor to navigate through the magnified image</p>
   "
>
   <img src="${base}/images/question-circle.png">
</a>

<img id="base-image" style="max-width: 100%" class="baseImage" src="${url}">

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>

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

    var heightThreshold = 200;

    var wrapped = false;

    ## Enable the zoom feature only for desktop browsers
    if (!$.browser.mobile) {

        var popoverBuffer = $("#popover-buffer");
        var popoverContent = $("#popover-content");

        popoverBuffer.css({
            "height": "38px"
        });

        popoverContent.css({
            "position": "absolute",
            "top": "10px",
            "right": "10px",
            "cursor": "pointer"
        });

        $('[data-toggle="popover"]').popover();

        $(document).ready(function() {

            var is_chrome = !!window.chrome;

            var baseImage = $("#base-image");

            var addSpan = function() {

                if (!wrapped) {

                    var baseImageHeight = parseInt(baseImage.css("height"));
                    var baseImageWidth = parseInt(baseImage.css("width"));

                    ## Quirk 1
                    ##
                    ## The BASE image must be wrapped with a parent "container" and it must be the
                    ## only image in this parent.  The "JQuery Zoom" library performs the zoom
                    ## function on the parent, in which it uses the first image it finds to create
                    ## the ZOOM image.
                    ##
                    ## There are two issues if it is not wrapped. First, the ZOOM image will be the
                    ## question cirle, which is the first image we have in the iframe. Second, the
                    ## ZOOM image will take over the full space of the iframe.
                    ##
                    ## Quirk 2
                    ##
                    ## Wrapping <img> with <div> or <span> in Google Chrome makes the scroll bar in
                    ## the <iframe> flickering when zoom is active. However, wrap it with <p> does
                    ## not have the problem for most of the time.
                    ##
                    ## Quirk 3
                    ##
                    ## Weird behaviors SOMETIMES occur when the image is downsized due to smaller
                    ## screen size. Thus, different wrapping are used.
                    ##
                    ## Quirk 4
                    ##
                    ## Werid behaviors ALWAYS occur when the image's height is less than 150. This
                    ## number is obtained by experiments. Thus, zoom are disabled for such images.
                    ##
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
                        baseImage.wrap("<p></p>")
                    }

                    wrapped = true;
                }
            };

            var mouseZoom = function(event, delta) {

                ## Disable page scroll when the mouse cursor are above the image
                event.preventDefault();

                if (delta > 0) {
                    magScale += magStep;
                    magScale = magScale > maxScale ? maxScale : magScale
                } else {
                    magScale -= magStep;
                    magScale = magScale < minScale ? minScale : magScale
                }

                var image = $(".zoomImage");
                magHeight = magHeight === null ? parseInt(image.css("height")) : magHeight;
                magWidth = magWidth === null ? parseInt(image.css("width")) : magWidth;

                image.css({
                    width: magWidth * magScale,
                    height: magHeight * magScale
                });
            };

            ## Create an in memory copy of the image to avoid CSS issues, TODO: double check
            $("<img>").attr("src", $(baseImage[0]).attr("src")).load(function() {

                widthLimit = this.width;
                heightLimit = this.height;

                ## Enable zoom and display popover instructions only when images are eligible
                if (heightLimit >= heightThreshold) {
                    $(window).resize(addSpan);
                    $("#popover-buffer").css("display", "block");
                    $("#popover-content").css("display", "block");
                    addSpan();
                    baseImage.parent().zoom({magnify: magScale}).on("mousewheel", mouseZoom);
                }
            });
        });
    }
</script>
