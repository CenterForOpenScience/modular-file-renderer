<script src="/static/js/jquery-1.11.3.min.js"></script>

<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css"/>
<script src="/static/js/bootstrap.min.js"></script>

## Quirks 0:
##
## The "bootstrap collapse" works OK.  However, a scroll bar appears and the image gets cut off when
## the list is expanded.  To see the full image, users need to grab the scroll bar to scroll down
## since the zoom feature disables page scroll when the cursor is above the image.
## TODO: during or after prod demo, discuss whether to live with it or to find alternatives
##
## <div id="msg-heading" class="alert alert-info" role="alert" style="display: none">
##     <span data-toggle="collapse" data-trigger="hover" data-target="#msg-content">
##         Need help zooming <img src="${base}/images/question-circle.png">
##     </span>
##     <ul id="msg-content" class="collapse">
##         <li>Click on the image to enable zoom and view the high-res version if available</li>
##         <li>Move mouse cursor to navigate and scroll the mouse wheel to zoom</li>
##         <li>Download the image to view it in its original size and format</li>
##     </ul>
## </div>
##
## Currently, display the full instructions on the top of the <iframe>
##
<div id="msg-heading" class="alert alert-info" role="alert" style="display: none">
    <p>How to zoom <img id="icon-question" src="${base}/images/question-circle.png"/></p>
    <ul>
        <li>Click on the image to enable zoom and view the high-res version if available</li>
        <li>Move mouse cursor to navigate and scroll the mouse wheel to zoom</li>
        <li>Download the image to view it in its original size and format</li>
    </ul>
</div>

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

    var heightThreshold = 150;

    var wrapped = false;

    ## Enable the zoom feature only for desktop browsers
    if (!$.browser.mobile) {

        var is_chrome = !!window.chrome;

        var message = $("#msg-heading");
        message.css({
            "font-size": "12px",
            "padding": "5px 5px 5px 5px",
            "white-space": "nowrap"
        });

        $(document).ready(function() {

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
                    ## If not wrapped, two issues are going to occure. First, the ZOOM image will be
                    ## the question cirle image, which is the first image we have in the iframe.
                    ## Second, the ZOOM image will take over the full space of the iframe.
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
                    ## TODO: double check
                    ##
                    ## Quirk 4
                    ##
                    ## Werid behaviors ALWAYS occur when the image's height is less than 150. This
                    ## number is obtained by experiments. Thus, zoom are disabled for such images.
                    ## TODO: double check
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

                ## Enable zoom and display instructions only when images are eligible
                if (heightLimit >= heightThreshold) {
                    $(window).resize(addSpan);
                    var message = $("#msg-heading");
                    message.css("display", "inline-block");
                    addSpan();
                    baseImage.parent().zoom({magnify: magScale}).on("mousewheel", mouseZoom);
                }
            });
        });
    }
</script>
