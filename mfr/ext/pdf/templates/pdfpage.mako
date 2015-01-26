
<span>Page: <span id="pageNum"></span> / <span id="pageCount"></span></span><br>

<div >
    <table style"width:inherit">
        <tr>
            <td style="width: 25px">
                <button unselectable="on" id="previousButton" class="mfr-pdf-button">
                    <img src="${STATIC_PATH}/pdf/images/leftarrow.png" style="width: 25px;">
                </button>
            </td>
            <td><canvas id="the-canvas" style="border:1px solid black;"></canvas></td>
            <td style="width: 25px">
                <button unselectable="on" id="nextButton" class="mfr-pdf-button">
                    <img src="${STATIC_PATH}/pdf/images/rightarrow.png" style="width: 25px;">
                </button>
            </td>
        </tr>
    </table>
</div>

<script type="text/javascript">
    // TODO: Figure out why we have to do this

(function(){
    PDFJS.workerSrc = '${STATIC_PATH}/pdf/js/pdf.worker.js';
    var url = "${url}";
    PDFJS.disableWorker = true;
    var pdfDoc = null,
        pageNum = 1,
        scale = 1.15,
        canvas = document.getElementById('the-canvas'),
        ctx = canvas.getContext('2d');

    //
    // Get page info from document, resize canvas accordingly, and render page
    //

    var $prevButton = $('#previousButton');
    var $nextButton = $("#nextButton");


    function renderPage(num) {
        // Using promise to fetch the page

        pdfDoc.getPage(num).then(function(page) {
            var viewport = page.getViewport(scale);
            canvas.height = viewport.height;
            canvas.width = viewport.width;


            // Render PDF page into canvas context
            var renderContext = {
                canvasContext: ctx,
                viewport: viewport
            };

            var navBarHeight = viewport.height;

            $prevButton.css({"height": navBarHeight});
            $nextButton.css({"height": navBarHeight});

            page.render(renderContext);
      });

    pageNum === 1 ? disableButton($prevButton) : setTimeout(function(){enableButton($prevButton)},250);
    pageNum === pdfDoc.numPages ? disableButton($nextButton) : setTimeout(function(){enableButton($nextButton)},250);


      // Update page counters
      document.getElementById('pageNum').textContent = pageNum;
      document.getElementById('pageCount').textContent = pdfDoc.numPages;
    }

    function disableButton($elem) {
        $elem[0].disabled = true;
        var $arrow = $elem.find('.mfr-pdf-button').addClass('disabled');
    }

    function enableButton($elem) {
        $elem[0].disabled = false;
        var $arrow = $elem.find('.mfr-pdf-button').removeClass('disabled');
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

