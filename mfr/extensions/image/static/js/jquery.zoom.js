/**
 * A plugin to enlarge images on touch, click, or mouseover.
 *
 * Original Copy: https://github.com/jackmoore/zoom/blob/1.7.20/jquery.zoom.js
 * Version: https://github.com/jackmoore/zoom/releases/tag/1.7.20
 *
 * The are three MFR customizations in this file, two for style and one for functionality
 *
 * 1. Updated code style according to `.eslintrc.js`
 * 2. Added `.on("mousewheel", function (e) { ... })` to enable further zoom by mouse wheel scroll
 * 3. Set "background-color: white" for "zoomImage" to handle images with transparent background
 */

(function ($) {

    "use strict";

    var defaults = {
        url: false,
        callback: false,
        target: false,
        duration: 120,
        on: "mouseover",
        touch: true,
        onZoomIn: false,
        onZoomOut: false,
        magnify: 1
    };

    // Core Zoom Logic, independent of event listeners.
    $.zoom = function(target, source, img, magnify) {

        var targetHeight,
            targetWidth,
            sourceHeight,
            sourceWidth,
            xRatio,
            yRatio,
            offset,
            $target = $(target),
            position = $target.css("position"),
            $source = $(source);

        // The parent element needs positioning so that the zoomed element can be correctly
        // positioned within.
        target.style.position = /(absolute|fixed)/.test(position) ? position : "relative";
        target.style.overflow = "hidden";
        img.style.width = img.style.height = "";

        $(img)
            .addClass("zoomImage")
            .css({
                position: "absolute",
                top: 0,
                left: 0,
                opacity: 0,
                "background-color": "white",
                width: img.width * magnify,
                height: img.height * magnify,
                border: "none",
                maxWidth: "none",
                maxHeight: "none"
            }).appendTo(target);

        return {
            init: function() {
                targetWidth = $target.outerWidth();
                targetHeight = $target.outerHeight();

                if (source === target) {
                    sourceWidth = targetWidth;
                    sourceHeight = targetHeight;
                } else {
                    sourceWidth = $source.outerWidth();
                    sourceHeight = $source.outerHeight();
                }

                xRatio = (img.width - targetWidth) / sourceWidth;
                yRatio = (img.height - targetHeight) / sourceHeight;

                offset = $source.offset();
            },
            move: function (e) {
                var left = (e.pageX - offset.left),
                    top = (e.pageY - offset.top);

                top = Math.max(Math.min(top, sourceHeight), 0);
                left = Math.max(Math.min(left, sourceWidth), 0);

                img.style.left = (left * -xRatio) + "px";
                img.style.top = (top * -yRatio) + "px";
            }
        };
    };

    $.fn.zoom = function (options) {

        return this.each(function () {

            var
                settings = $.extend({}, defaults, options || {}),
                //Target will display the zoomed image
                target = settings.target && $(settings.target)[0] || this,
                //Source will provide zoom location info (thumbnail)
                source = this,
                $source = $(source),
                img = document.createElement("img"),
                $img = $(img),
                mousemove = "mousemove.zoom",
                clicked = false,
                touched = false;

            // If a url wasn't specified, look for an image element.
            if (!settings.url) {
                var srcElement = source.querySelector("img");
                if (srcElement) {
                    settings.url = srcElement.getAttribute("data-src") ||
                        srcElement.currentSrc || srcElement.src;
                }
                if (!settings.url) {
                    return;
                }
            }

            $source.one("zoom.destroy", function(position, overflow) {
                $source.off(".zoom");
                target.style.position = position;
                target.style.overflow = overflow;
                img.onload = null;
                $img.remove();
            }.bind(this, target.style.position, target.style.overflow));

            img.onload = function () {

                var zoom = $.zoom(target, source, img, settings.magnify);

                function start(e) {
                    zoom.init();
                    zoom.move(e);
                    // Skip the fade-in for IE8 and lower. It chokes on fading-in and changing
                    // position based on mousemovement at the same time.
                    $img.stop().fadeTo(
                        $.support.opacity ? settings.duration : 0, 1, $.isFunction(settings.onZoomIn) ? settings.onZoomIn.call(img) : false
                    );
                }

                function stop() {
                    $img.stop().fadeTo(
                        settings.duration, 0, $.isFunction(settings.onZoomOut) ? settings.onZoomOut.call(img) : false
                    );
                }

                // Mouse events
                if (settings.on === "grab") {

                    $source.on("mousedown.zoom", function (e) {
                        if (e.which === 1) {
                            $(document).one("mouseup.zoom", function () {
                                stop();
                                $(document).off(mousemove, zoom.move);
                            });
                            start(e);
                            $(document).on(mousemove, zoom.move);
                            e.preventDefault();
                        }
                    });

                } else if (settings.on === "click") {

                    $source.on("click.zoom", function (e) {
                        if (!clicked) {
                            clicked = true;
                            start(e);
                            $(document).on(mousemove, zoom.move);
                            $(document).one("click.zoom",
                                function () {
                                    stop();
                                    clicked = false;
                                    $(document).off(mousemove, zoom.move);
                                }
                            );
                            return false;
                        }
                        // do nothing if clicked is true, bubble the event up to the document to
                        // trigger the unbind.
                    });

                    // MFR customization: Allow further zoom using mouse wheel on the zoom image.
                    // The zoom is only enabled when image is clicked.  I am not entirely sure how
                    // `stop()` works but having it inside or outside the `if (clicked) { ... }`
                    // statement does not make a difference.  TODO: need more investigation
                    $source.on("mousewheel", function (e) {
                        stop();
                        if (clicked) {
                            start(e);
                        }
                    });

                } else if (settings.on === "toggle") {

                    $source.on("click.zoom", function (e) {
                        if (clicked) {
                            stop();
                        } else {
                            start(e);
                        }
                        clicked = !clicked;
                    });

                } else if (settings.on === "mouseover") {

                    // Preemptively call zoom.init() because IE7 will fire the mousemove handler
                    // before the hover handler.
                    zoom.init();
                    $source.on("mouseenter.zoom", start)
                        .on("mouseleave.zoom", stop)
                        .on(mousemove, zoom.move);
                }

                // Touch fallback
                if (settings.touch) {

                    $source.on("touchstart.zoom", function (e) {
                        e.preventDefault();
                        if (touched) {
                            touched = false;
                            stop();
                        } else {
                            touched = true;
                            start(e.originalEvent.touches[0] || e.originalEvent.changedTouches[0]);
                        }
                    }).on("touchmove.zoom", function (e) {
                        e.preventDefault();
                        zoom.move(e.originalEvent.touches[0] || e.originalEvent.changedTouches[0]);
                    }).on("touchend.zoom", function (e) {
                        e.preventDefault();
                        if (touched) {
                            touched = false;
                            stop();
                        }
                    });
                }

                if ($.isFunction(settings.callback)) {
                    settings.callback.call(img);
                }
            };

            img.setAttribute("role", "presentation");
            img.src = settings.url;
        });
    };

    $.fn.zoom.defaults = defaults;
}(window.jQuery));
