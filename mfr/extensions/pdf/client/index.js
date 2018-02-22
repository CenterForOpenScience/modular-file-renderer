
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

import {
    PDFJS
} from "pdfjs-lib";


import {PDFViewerApplication} from "pdfjs-web/app";

// hypothes.is expects the object to be global.
window.PDFViewerApplication = PDFViewerApplication;

import {
    parseQueryString,
    noContextMenuHandler,
} from 'pdfjs-web/ui_utils';

PDFViewerApplication.run = function(config) {
    this.initialize(config).then(webViewerInitialized);
}

PDFViewerApplication.initialize = function(appConfig) {
    this.preferences = this.externalServices.createPreferences();

    PDFJS.imageResourcesPath = './images/';
    PDFJS.workerSrc = "assets/pdf.worker.js";
    PDFJS.cMapUrl = '../web/cmaps/';
    PDFJS.cMapPacked = true;
    appConfig.defaultUrl = DEFAULT_URL;
    this.appConfig = appConfig;

    return this._readPreferences().then(() => {
      return this._initializeL10n();
    }).then(() => {
      return this._initializeViewerComponents();
    }).then(() => {
        // Bind the various event handlers *after* the viewer has been
        // initialized, to prevent errors if an event arrives too soon.
        this.bindEvents();
        this.bindWindowEvents();
        // We can start UI localization now.
        let appContainer = appConfig.appContainer || document.documentElement;
        this.l10n.translate(appContainer).then(() => {
            // Dispatch the 'localized' event on the `eventBus` once the viewer
            // has been fully initialized and translated.
            this.eventBus.dispatch('localized');
        });

        if (this.isViewerEmbedded && !PDFJS.isExternalLinkTargetSet()) {
            // Prevent external links from "replacing" the viewer,
            // when it's embedded in e.g. an iframe or an object.
            PDFJS.externalLinkTarget = PDFJS.LinkTarget.TOP;
        }

        this.initialized = true;
    });
}

function webViewerInitialized() {

    let appConfig = PDFViewerApplication.appConfig;
    let file;
    let queryString = document.location.search.substring(1);
    let params = parseQueryString(queryString);
    file = 'file' in params ? params.file : appConfig.defaultUrl;
    validateFileURL(file);
    let fileInput = document.createElement('input');

    fileInput.id = appConfig.openFileInputName;
    fileInput.className = 'fileInput';
    fileInput.setAttribute('type', 'file');
    fileInput.oncontextmenu = noContextMenuHandler;

    document.body.appendChild(fileInput);
    if (!window.File || !window.FileReader ||
        !window.FileList || !window.Blob) {
        appConfig.toolbar.openFile.setAttribute('hidden', 'true');
        appConfig.secondaryToolbar.openFileButton.setAttribute('hidden', 'true');
    } else {
        fileInput.value = null;
    }

    fileInput.addEventListener('change', function(evt) {
        let files = evt.target.files;
        if (!files || files.length === 0) {
            return;
        }
        PDFViewerApplication.eventBus.dispatch('fileinputchange', {
            fileInput: evt.target,
        });
    });

    if (!PDFViewerApplication.supportsPrinting) {
        appConfig.toolbar.print.classList.add('hidden');
        appConfig.secondaryToolbar.printButton.classList.add('hidden');
    }

    if (!PDFViewerApplication.supportsFullscreen) {
        appConfig.toolbar.presentationModeButton.classList.add('hidden');
        appConfig.secondaryToolbar.presentationModeButton.classList.add('hidden');
    }

    if (PDFViewerApplication.supportsIntegratedFind) {
        appConfig.toolbar.viewFind.classList.add('hidden');
    }

    appConfig.mainContainer.addEventListener('transitionend', function(evt) {
        if (evt.target === /* mainContainer */ this) {
            PDFViewerApplication.eventBus.dispatch('resize', { source: this, });
        }
    }, true);

    appConfig.sidebar.toggleButton.addEventListener('click', function() {
        PDFViewerApplication.pdfSidebar.toggle();
    });

    Promise.resolve().then(function() {
        webViewerOpenFileViaURL(file);
    }).catch(function(reason) {
        PDFViewerApplication.l10n.get('loading_error', null,
        'An error occurred while loading the PDF.').then((msg) => {
            PDFViewerApplication.error(msg, reason);
        });
    });
}

let validateFileURL;
if (typeof PDFJSDev === 'undefined' || PDFJSDev.test('GENERIC')) {
    const HOSTED_VIEWER_ORIGINS = [
        'null',
        'http://mozilla.github.io',
        'https://mozilla.github.io',
        "http://localhost:7778"
    ];
    validateFileURL = function validateFileURL(file) {
        if (file === undefined) {
            return;
        }
        try {
            let viewerOrigin = new URL(window.location.href).origin || 'null';
            if (HOSTED_VIEWER_ORIGINS.includes(viewerOrigin)) {
                // Hosted or local viewer, allow for any file locations
                return;
            }
            let fileOrigin = new URL(file, window.location.href).origin;
            // Removing of the following line will not guarantee that the viewer will
            // start accepting URLs from foreign origin -- CORS headers on the remote
            // server must be properly configured.
            if (fileOrigin !== viewerOrigin) {
                throw new Error('file origin does not match viewer\'s');
            }
        } catch (ex) {
            let message = ex && ex.message;
            PDFViewerApplication.l10n.get(
                'loading_error',
                null,
                'An error occurred while loading the PDF.'
            ).then((loadingErrorMessage) => {
                PDFViewerApplication.error(loadingErrorMessage, { message, });
            });
            throw ex;
        }
    };
}

let webViewerOpenFileViaURL;
if (typeof PDFJSDev === 'undefined' || PDFJSDev.test('GENERIC')) {
  webViewerOpenFileViaURL = function webViewerOpenFileViaURL(file) {
    if (file && file.lastIndexOf('file:', 0) === 0) {
      // file:-scheme. Load the contents in the main thread because QtWebKit
      // cannot load file:-URLs in a Web Worker. file:-URLs are usually loaded
      // very quickly, so there is no need to set up progress event listeners.
      PDFViewerApplication.setTitleUsingUrl(file);
      let xhr = new XMLHttpRequest();
      xhr.onload = function() {
        PDFViewerApplication.open(new Uint8Array(xhr.response));
      };
      try {
        xhr.open('GET', file);
        xhr.responseType = 'arraybuffer';
        xhr.send();
      } catch (ex) {
        throw ex;
      }
      return;
    }

    if (file) {
      PDFViewerApplication.open(file, {withCredentials: true});
    }
  };
} else if (PDFJSDev.test('FIREFOX || MOZCENTRAL || CHROME')) {
  webViewerOpenFileViaURL = function webViewerOpenFileViaURL(file) {
    PDFViewerApplication.setTitleUsingUrl(file);
    PDFViewerApplication.initPassiveLoading();
  };
} else {
  webViewerOpenFileViaURL = function webViewerOpenFileViaURL(file) {
    if (file) {
      throw new Error('Not implemented: webViewerOpenFileViaURL');
    }
  };
}

import viewer from 'pdfjs-web/viewer';


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
