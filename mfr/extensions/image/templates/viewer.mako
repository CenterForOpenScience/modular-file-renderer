<script src="/static/js/jquery-1.11.3.min.js"></script>

<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css"/>
<script src="/static/js/bootstrap.min.js"></script>

## The block to hold the question circle, which prevents it from overlapping with the image and
## of which the style will be updated if zoom is enabled
<div id="popover-buffer" style="display: none"></div>
<a id="popover-content" style="display: none" data-toggle="popover"
   data-trigger="hover" data-placement="left" data-html="true"
   data-content="
    <p><b> HiRes:</b> Click on the image to view in higher resolution when available</p>
    <p><b> Zoom:</b> Click on the image and use the mouse wheel to zoom in and out</p>
    <p><b> Navigate:</b> Move the mouse cursor to navigate through the magnified image</p>
   "
><img src="${base}/images/question-circle.png"></a>

## The image to render, which will be wrapped accordingly if zoom is enabled
<img id="base-image" style="max-width: 100%" class="baseImage" src="${url}">

## MFR scripts
<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>

## JQuery Zoom and Mouse Wheel scripts
<script src="${base}/js/jquery.mousewheel.min.js"></script>
<script src="${base}/js/jquery.zoom.js"></script>

## The main script for enable Hi-Res and Zoom for rendered images
<script>
    ## Enforces strict mode
    "use strict";

    ## Magnifiation parameters
    var magScale = 1;
    var magStep = 0.1;
    var maxScale = 3;
    var minScale = 1;
    var magHeight = null;
    var magWidth = null;

    ## The height and width for the displaying part of the image
    var heightLimit = null;
    var widthLimit = null;

    ## The minimal height requirement to enable the zoom feature for a image
    ## For more information, refer to the line where it is used in this file
    var minHeightToZoom = 200;

    ## A flag indicating whether the image is already wrapped or not
    var wrapped = false;

    $(document).ready(function() {

        ## Reference on how mobile is detected: https://stackoverflow.com/a/10364620
        var isMobile = window.matchMedia("only screen and (max-width: 760px)");

        ## Enable the zoom feature only for desktop browsers
        if (!isMobile.matches) {

            ## Update the style for instruction popover and enable it
            var popoverBuffer = $("#popover-buffer");
            var popoverContent = $("#popover-content");
            popoverBuffer.css({"height": "38px"});
            popoverContent.css({
                "position": "absolute",
                "top": "10px",
                "right": "10px",
                "cursor": "pointer"
            });
            $('[data-toggle="popover"]').popover();

            var baseImage = $("#base-image");

            ## Quirks: the base image must be wrapped, see http://www.jacklmoore.com/zoom/
            ##
            ## The BASE image must be wrapped with a parent "container" and it must be the only (or
            ## the first) image in it.  The `jquery.zoom` library performs the zoom on the parent
            ## and grabs the first image it finds to create the zoom image.
            ##
            ## `addSpan()` performs the "wrap" accordingly to cater for most cases
            var addSpan = function () {

                ## Only wrap the image once
                if (wrapped) {
                    return;
                }

                ## Obtain the original height and width for the image loaded
                var baseImageHeight = parseInt(baseImage.css("height"), 10);
                var baseImageWidth = parseInt(baseImage.css("width"), 10);

                ## Detect the Google Chrome browser
                var isChrome = !!window.chrome;

                ## Detect if the image is downsized due to screen size
                var isActualSize = heightLimit === baseImageHeight || widthLimit === baseImageWidth;

                if (isActualSize || !isChrome) {
                    ## Use the default wrapping suggested by http://www.jacklmoore.com/zoom/ if
                    ## either of the two conditions below holds:
                    ## 1.   Images are downsized but not in Google Chrome. Please see the flickering
                    ##      issue mentioned below.
                    ## 2.   Images are displayed in its actual size. No issue for all supported
                    ##      browsers.
                    baseImage.wrap("<div></div>").parent().css({
                        "display": "inline-block",
                        "max-width": "100%",  // need to be explicit for IE
                        "height": "auto"      // need to be explicit for IE
                    });
                } else {
                    ## Quirks: Chrome has a flickering bug when images are wrapped with `<div>` or
                    ## `<span>`.  During zoom the scroll bar keeps appearing and disappearing which
                    ## causes the image to keep resizing.  Wrapping with `<p>` instead to solve this
                    ## annoying issue.
                    baseImage.wrap("<p></p>")
                }

                wrapped = true;
            };

            var mouseZoom = function (event, delta) {

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
                magHeight = magHeight === null ? parseInt(image.css("height"), 10) : magHeight;
                magWidth = magWidth === null ? parseInt(image.css("width"), 10) : magWidth;

                image.css({
                    width: magWidth * magScale,
                    height: magHeight * magScale
                });
            };

            ## Quirks: Need to use an in-memory copy of the image to prevent the zoom image from
            ##         moving around.  Without this in-memoery copy, the zoom image moves around
            ##         horizontally and "centers" wherever the mouse cursor is.
            $("<img>").attr("src", $(baseImage[0]).attr("src")).load(function () {

                widthLimit = this.width;
                heightLimit = this.height;

                ## Quirks: Disable zoom and display instructions for images of height less than 200.
                ## 1.   The original issue was when the height is less than 150 (not 200), the zoom
                ##      image moves around and thus does not cover the base image fully. However,
                ##      I cannot trigger this any more.
                ## 2.   When the height is less than around 200 (a little bit less than 200), which
                ##      is close to the height of the popover instruction when shown, the bottom
                ##      part of the instruction block is cut off.  Users need to scroll down to see
                ##      the full message.  In addition, the scroll bar overlaps with the question
                ##      circle.
                ## 3.   Images of height less than 200 are not worth zooming anyway.
                if (heightLimit < minHeightToZoom) {
                    return;
                }

                ## For images that are eligible to zoom:
                ## 1. Display the question circle for popover zoom instructions
                ## 2. Wrap the base image accordingly by calling `addSpan()`
                ## 3. Call zoom on its parent with customized configs (scale and mouse click)
                ## 4. Enable further zoom on mouse wheel
                $(window).resize(addSpan);
                $("#popover-buffer").css("display", "block");
                $("#popover-content").css("display", "block");
                addSpan();
                baseImage.parent().zoom({magnify: magScale, on: 'click'}).on("mousewheel", mouseZoom);
            });
        }
    });
</script>
