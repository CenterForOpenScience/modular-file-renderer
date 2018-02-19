import pdfjsLib from "pdfjs-lib";

/*PDFViewerApplication.setTitleUsingUrl = function(url) {

    this.url = url;

    var rel_canonical = document.createElement('link');
    rel_canonical.href = url;
    rel_canonical.rel = "canonical";
    document.head.appendChild(rel_canonical);

    this.baseUrl = url.split('#')[0];
    let title = getPDFFileNameFromURL(url, '');
    if (!title) {
      try {
        title = decodeURIComponent(getFilenameFromUrl(url)) || url;
      } catch (ex) {
        // decodeURIComponent may throw URIError,
        // fall back to using the unprocessed url in that case
        title = url;
      }
    }

    this.setTitle(title);

};*/

import viewer from 'pdfjs-web/viewer';

console.log(viewer);
debugger;

// Any copyright is dedicated to the Public Domain.
// http://creativecommons.org/licenses/publicdomain/

// Hello world example for webpack.


/*
var pdfPath = '../helloworld/helloworld.pdf';

// Setting worker path to worker bundle.
pdfjsLib.PDFJS.workerSrc = '../../build/webpack/pdf.worker.bundle.js';

// Loading a document.
var loadingTask = pdfjsLib.getDocument(pdfPath);
loadingTask.promise.then(function (pdfDocument) {
  // Request a first page
  return pdfDocument.getPage(1).then(function (pdfPage) {
    // Display page on the existing canvas with 100% scale.
    var viewport = pdfPage.getViewport(1.0);
    var canvas = document.getElementById('theCanvas');
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    var ctx = canvas.getContext('2d');
    var renderTask = pdfPage.render({
      canvasContext: ctx,
      viewport: viewport
    });
    return renderTask.promise;
  });
}).catch(function (reason) {
  console.error('Error: ' + reason);
});
*/
