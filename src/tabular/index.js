import "../mfr/child";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.css";
import "../style/slick.grid.css";
import "../style/examples.css";
import "../style/slick-default-theme.css";
import {Slick} from "slickgrid-es6";

var sheets = window.sheets;
var options = window.options;
var gridArr = {};
var grid;
var data;
var searchString = "";

for (var sheetName in sheets){
    var sheet = sheets[sheetName];
    sheetName = sheetName.replace( /(:|\.|\[|\]|,|@|&|\ )/g, '_' ); //Handle characters that can't be in DOM ID's
    $("#tabular-tabs").append('<li role="presentation" style="display:inline-block; float: none;"><a id="' + sheetName + '" aria-controls="' + sheetName + '" role="tab" data-toggle="tab">'+ sheetName + '</a></li>');
    gridArr[sheetName] = [sheet[0], sheet[1]];

    $('#'+sheetName).click(function (e) {
        e.preventDefault();
        var columns = gridArr[$(this).attr('id')][0];
        var rows = gridArr[$(this).attr('id')][1];

        grid = new Slick.Grid('#mfrGrid', rows, columns, options);
        searchString = "";
        $("#txtSearch").value = "";
        data = grid.getData();
        grid.onSort.subscribe(sortData);
    });
}

$("#tabular-tabs").tab();
$("#tabular-tabs a:first").click();

$("#txtSearch").keyup(function (e) {
    // clear on Esc
    if (e.which == 27) {
      this.value = "";
    }
    searchString = this.value;
    var filteredData = (searchString !== "") ? filterData(data, searchString) : data;
    grid = new Slick.Grid('#mfrGrid', filteredData, grid.getColumns(), options);
    grid.onSort.subscribe(sortData);
});

$(".list").on('scroll', function (e) {
    reAdjust();
});

$(window).resize(function () {
    reAdjust();
});

function filterData(data, search) {
    var filteredData = [];
    var re = new RegExp(search, 'i');
    for (var i = 0; i<data.length; i++){
        var filtered = false;
        var item = data[i];
        for (var title in item) {
            if (search !== '' && item[title].toString().match(re)) {
                filtered = filtered || true;
                continue;
            }
        }
        if (filtered){
            filteredData.push(item);
        }
    }
    return filteredData;
}

function probablyANumber(s) {
    // Guess whether something is a number.  isNaN coerces its argument into a Number.
    // Most non-numeric strings will return NaN, including "3.14abc".  Special care must
    // be taken with non-numeric things that can be cast to Numbers e.g. true, false, null,
    // "", "      ", etc.  For more information see:
    //
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/isNaN
    //
    // This is called probablyANumber because I'm sure we've omitted some special case.
    return !isNaN(s) && s !== null && s !== "" && s !== false && s !== true &&
           !/^ +$/.test(s);
}

function prepareSortValue(s) {
    // Everything retrieved from SlickGrid is a string.
    // If those strings are numbers, parse them.
    if (probablyANumber(s)) {
        return parseFloat(s);
    }
    return s;
}

function sortData (e, args) {
    var cols = args.sortCols;
    var rows = grid.getData();
    rows.sort(function (dataRow1, dataRow2) {
        for (var i = 0; i < cols.length; i++) {
            var field = cols[i].sortCol.field;
            var sign = cols[i].sortAsc ? 1 : -1;
            var value1 = prepareSortValue(dataRow1[field]);
            var value2 = prepareSortValue(dataRow2[field]);
            var result = (value1 == value2 ? 0 : (value1 > value2 ? 1 : -1)) * sign;
            if (result !== 0) {
                return result;
            }
        }
        return 0;
    });
    grid.invalidate();
    grid.render();
}

function reAdjust(){
    let liFirstPosLeft = $('.list li:first').position().left;
    let liLastPosRight = $('.list li:last').position().left + $('.list li:last').width();
    let widthOfList = $('.list').width();
    if (liFirstPosLeft < 0) {
        $('.scroller-left').show();
    }
    else {
        $('.scroller-left').hide();
    }

    if ((liLastPosRight - 2) < widthOfList) {  // The end of the list is consistently 1.9333 pixels off
        $('.scroller-right').hide();
    }
    else {
        $('.scroller-right').show();
    }
}

reAdjust();

