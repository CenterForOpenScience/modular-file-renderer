

<!-- Blurb about how to use controls/functionality should go here -->
<div id="zoomInstructions" style="visibility: hidden;"> </div>


<img style="max-width: 100%;" class='baseImage' src="${url}">

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
<script src="/static/js/jquery-1.11.3.min.js"></script>
<script src="${base}/js/jquery.mousewheel.min.js"></script>
<script src="${base}/js/jquery.zoom.js"></script>

<script>
    // Use user agent string to try and find mobile users. Not always reliable, but other methods have more overhead.
    // This method should probably be replaced at some point.
    (function(a){(jQuery.browser=jQuery.browser||{}).mobile=/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))})(navigator.userAgent||navigator.vendor||window.opera);

    var magnification = 1;
    var magHeight = null;
    var magWidth = null;
    var inLined = false;
    var widthLimit = null;
    var heightLimit = null;

    // dont want to use zoom.js for mobile
    if(! $.browser.mobile){

        $(document).ready(function(){
          var baseImage= $('.baseImage');
            
            // images of certain sizes need in-blocks added to them so they display right and dont act weird
            // however other images can't have inline blocks because it bugs out on chrome horribly
            // with scrollbar flickering. This will determine if we need to add inlining, and add
            // it at appropriate times so weird behavior and scrollbar flickering wont happen.
            var addSpan = function(){
                if(!inLined){
                    if(heightLimit === parseInt(baseImage.css('height')) || widthLimit === parseInt(baseImage.css('width'))){
                        baseImage
                        // needed as a buffer to not break #zoomInstructions
                            .wrap('<div style="position: relative; overflow: hidden; display: block;" ></div>');
                        baseImage
                            .parent()
                            .wrap('<span style="display:inline-block"></span>')
                            .css('display', 'block');
                        inLined = true;
                    }
                }
            }

            // custom code to add zoom in on mouse scroll. Might want to check 
            // what product wants the controls to be for sure. maybe shift scroll?
            var mouseFunction = function(event, delta) {
                // stops page from scrolling while zooming image
                event.preventDefault();

                if(delta > 0){ // mouse wheel direction
                    magnification += .1;
                    // max magnification is 3x source image size. Might want to make this variable
                    // to a certain max size, ie 3k x3k or whatever.
                    if (magnification > 3){
                        magnification = 3;
                    }
                }
                else{
                    magnification -= .1;
                    // min zoom, could be variable based on source size vs regular display size.
                    // you dont want to make image too small, then you will see 2 of them.
                    // might want to fade out base image when the zoom one is displayed
                    if (magnification < 1){
                        magnification = 1;
                    }
                }
                
                var img = $('.zoomImg');

                if (magHeight === null && magWidth === null){
                    magWidth = parseInt(img.css('width')) 
                    magHeight = parseInt(img.css('height'))
                }
                img.css({
                    width: magWidth * magnification,
                    height:  magHeight * magnification,
                });
            }
            
            $("<img/>") // Make in memory copy of image to avoid css issues
                .attr("src", $(baseImage[0]).attr("src"))
                .load(function() {
                    widthLimit = this.width;
                    heightLimit = this.height;
                    if (heightLimit >= 150){
                        $(window).resize(addSpan);
                        // display instructions if zoom is being used
                        $("#zoomInstructions").css('visibility', 'visible');
                        $("#zoomInstructions").html("Message on how to use should be styled and go here!!");
                        addSpan();
                        baseImage
                            .parent()
                            .zoom({ magnify: magnification})
                            .on('mousewheel', mouseFunction)
                    }
                });

        })
    }


</script>