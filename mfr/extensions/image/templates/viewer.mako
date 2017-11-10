
<img style="max-width: 100%;" class='baseImage' src="${url}">
<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>

<script src="/static/js/jquery-1.11.3.min.js"></script>
<script src="${base}/js/jquery.mousewheel.min.js"></script>

<script src="${base}/js/jquery.zoom.js"></script>

<script>
    var thing = 1;
    var magHeight = null;
    var magWidth = null;
    var inLined = false;
    var widthLimit = null;
    var heightLimit = null;

    $(document).ready(function(){
      var baseImage= $('.baseImage');
        var addSpan = function(){
            if(!inLined){
                if(heightLimit === parseInt(baseImage.css('height')) || widthLimit === parseInt(baseImage.css('width'))){
                    baseImage
                    .parent()
                    .wrap('<span style="display:inline-block"></span>')
                    .css('display', 'block');
                    inLined = true;
                }
            }
        }

        var mouseFunction = function(event, delta) {
            event.preventDefault();

            if(delta > 0){
                thing += .1;
                if (thing > 3){
                    thing = 3;
                }
            }
            else{
                thing -= .1;
                if (thing < .5){
                    thing = .5;
                }
            }
            
            var img = $('.zoomImg');

            if (magHeight === null && magWidth === null){
                magWidth = parseInt(img.css('width')) 
                magHeight = parseInt(img.css('height'))
            }
            
            img.css({
                width: magWidth * thing,
                height:  magHeight * thing,
            });
        }
        
        baseImage
            .parent()
            .zoom({ magnify: thing})
            .on('mousewheel', mouseFunction);

        $("<img/>") // Make in memory copy of image to avoid css issues
            .attr("src", $(baseImage[0]).attr("src"))
            .load(function() {
                widthLimit = this.width;
                heightLimit = this.height;
                if (heightLimit < 150){
                    baseImage.trigger('zoom.destroy');
                }
                else{
                    $(window).resize(addSpan);
                    addSpan();
                }
            });
    })


</script>