<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,600,300,700"
      rel="stylesheet" type="text/css">
<link rel="stylesheet" href="static/css/default.css">
<link rel="stylesheet" href="${base}/css/tdms.css">

<div class="row">
    <div class="column">
        <div class=titleBar>
            <h4>File Contents</h4>
        </div>
        <div class="belowTitle">
            <div class=miniTitleBar onclick="showHide('metadataContent','metadataButton')">
                <h5>File Metadata</h5>
                <p class='button' id='metadataButton'>-</p>
            </div>
            <div class="belowTitle">
                <div class="quadrant" id="topLeft">
                    <ul class="metadataContent">
                        ${fileMetadata}
                    </ul>
                </div>
            </div>
            <div class="quadrant" id="bottomLeft">
                <table id="propertyTable">
                    ${properties}
                </table>
            </div>
        </div>
    </div>
    <div class="column">
        <div class="quadrant" id="topRight">
            <div class=titleBar>
                <h4>Data Plot</h4>
            </div>
            <img id="plot" src=${plot}>
        </div>
        <div class="quadrant" id="bottomRight">
            <div class=titleBar>
                <h4>Data Table</h4>
            </div>
            <div class="belowTitle">
                ${table}
            </div>
        </div>
    </div>
</div>

<script src="/static/js/mfr.js"></script>
<script src="/static/js/mfr.child.js"></script>
<script src="${base}/js/tdms.js"></script>
