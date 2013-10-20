from .. import FileRenderer
import pandas
import json

class TabularRenderer(FileRenderer):

    def detect(self, fp):
        return fp.name.endswith('csv')

    def render(self, fp, path):
        return '''<table width="100%">
  <tr>
    <td valign="top" width="50%">
      <div id="myGrid" style="width:600px;height:500px;"></div>
    </td>
    <td valign="top">
    </td>
  </tr>
</table>'''


