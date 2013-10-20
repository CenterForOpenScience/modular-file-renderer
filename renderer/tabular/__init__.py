from .. import FileRenderer
import pandas as pd
import json

class TabularRenderer(FileRenderer):

    def detect(self, fp):
        return fp.name.endswith('csv')

    def render(self, fp, path):
        return '''
        <script src="../lib/jquery-1.7.min.js"></script>
        <script src="../lib/jquery.event.drag-2.2.js"></script>
        <script src="../slick.core.js"></script>
        <script src="../slick.grid.js"></script>
        <script>
            var grid;
var columns = [
    {   'field': 'employees', 'id': 'employees', 'name': 'employees'},
    {   'field': 'gender', 'id': 'gender', 'name': 'gender'},
    {   'field': 'desk', 'id': 'desk', 'name': 'desk'}];

  var options = {
    enableCellNavigation: true,
    enableColumnReorder: false
  };

  $(function () {
        <table width="100%">
  <tr>
    <td valign="top" width="50%">
      <div id="myGrid" style="width:600px;height:500px;"></div>
    </td>
    <td valign="top">
    </td>
  </tr>
</table>'''


