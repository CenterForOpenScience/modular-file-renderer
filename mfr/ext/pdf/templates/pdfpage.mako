<span>Page: <span id="pageNum"></span> / <span id="pageCount"></span></span><br>


<div style="width:auto">
    <nobr>
        <div id="leftDiv" style="display:inline-block; vertical-align: top;">
            <button unselectable="on" id="previousButton" class="mfr-pdf-button">
                <img id="leftArrow" class="mfr-pdf-arrow" src="${STATIC_PATH}/pdf/images/leftarrow.png" style="width: 25px;">
            </button>
        </div>

        <canvas id="the-canvas" style="border:1px solid black; width:95%"></canvas>

        <div id="rightDiv" style="display:inline-block; vertical-align: top;">
            <button unselectable="on" id="nextButton" class="mfr-pdf-button">
                <img id="rightArrow" class="mfr-pdf-arrow" src="${STATIC_PATH}/pdf/images/rightarrow.png" style="width: 25px;">
            </button>
        </div>
    </nobr>
</div>


<script type="text/javascript">
    // TODO: Figure out why we have to do this

(function(){
    PDFJS.workerSrc = '${STATIC_PATH}/pdf/js/pdf.worker.js';
    var url = "${url}";
    PDFJS.disableWorker = true;
    var pdfDoc = null,
        pageNum = 1,
        scale = 1.25,
        canvas = document.getElementById('the-canvas'),
        ctx = canvas.getContext('2d');

    //
    // Get page info from document, resize canvas accordingly, and render page
    //

    var $prevButton = $('#previousButton');
    var $nextButton = $("#nextButton");
    var $rightArrow = $("#rightArrow");
    var $leftArrow = $("#leftArrow");
    var $leftDiv = $("#leftDiv");
    var $rightDiv = $("#rightDiv");

    // Obtain a graphics context on the
    // canvas element for drawing.
    var context = canvas.getContext('2d');

    // Register an event listener to
    // call the resizeCanvas() function each time
    // the window is resized.
    window.addEventListener('resize', resizeCanvas, false);

    // Draw canvas border for the first time.
    resizeCanvas();

    // Runs each time the DOM window resize event fires.
    // Resets the canvas dimensions to match window,
    // then draws the new borders accordingly.
    function resizeCanvas() {
        var canvasHeight = $(canvas).height();
        var navBarHeight = canvasHeight + 2 + "px";
        $prevButton.css("height", navBarHeight);
        $nextButton.css("height",navBarHeight);
    }

    function renderPage(num) {
        // Using promise to fetch the page
        // TODO: Think of better approach for max size
        pdfDoc.getPage(num).then(function(page) {
            var viewport = page.getViewport(scale);
            if (viewport.width > 800) {
                adjScale = 800 / viewport.width;
                viewport = page.getViewport(adjScale);
            }
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            // Render PDF page into canvas context
            var renderContext = {
                canvasContext: ctx,
                viewport: viewport
            };
            var navBarHeight = viewport.height + 2 + "px";
            $prevButton.css("height", navBarHeight);
            $nextButton.css("height",navBarHeight);
            page.render(renderContext);
            resizeCanvas();
        });


        pageNum === 1 ? disableButton($prevButton) : setTimeout(function(){enableButton($prevButton)},1000);
        pageNum === pdfDoc.numPages ? disableButton($nextButton) : setTimeout(function(){enableButton($nextButton)},1000);


        // Update page counters
        document.getElementById('pageNum').textContent = pageNum;
        document.getElementById('pageCount').textContent = pdfDoc.numPages;
    }

    function disableButton($elem) {
        $elem[0].disabled = true;
        var $arrow = $elem.find('.mfr-pdf-arrow').addClass('disabled');
    }

    function enableButton($elem) {
        $elem[0].disabled = false;
        var $arrow = $elem.find('.mfr-pdf-arrow').removeClass('disabled');
    }



    //
    // Go to previous page
    //

    function goPrevious() {
        if (pageNum <= 1)
            return;
        pageNum--;

        renderPage(pageNum);
    }

    $prevButton.click(function(){
        disableButton($(this));
        goPrevious();
    });

    //
    // Go to next page
    //

    function goNext() {
        if (pageNum >= pdfDoc.numPages)
            return;
        pageNum++;
        renderPage(pageNum);
    }

    $nextButton.click(function(){
        goNext();
        disableButton($(this));
    });

    PDFJS.getDocument(url).then(function getPdf(_pdfDoc) {
      pdfDoc = _pdfDoc;
      renderPage(pageNum);
    });

})();
</script>