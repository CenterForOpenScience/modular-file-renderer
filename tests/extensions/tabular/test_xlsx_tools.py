import os

from mfr.extensions.tabular.libs import xlrd_tools

BASE = os.path.dirname(os.path.abspath(__file__))


class TestTabularPandaTools:

    def test_xlsx_xlrd(self):
        with open(os.path.join(BASE, 'files', 'test.xlsx')) as fp:
            sheets = xlrd_tools.xlsx_xlrd(fp)

        sheet = sheets.popitem()[1]
        assert sheet[0][0] == {'field': 'one', 'id': 'one', 'name': 'one', 'sortable': True}
        assert sheet[0][1] == {'field': 'two', 'id': 'two', 'name': 'two', 'sortable': True}
        assert sheet[0][2] == {'field': 'three', 'id': 'three', 'name': 'three', 'sortable': True}
        assert sheet[1][0] == {'one': 'a', 'two': 'b', 'three': 'c'}
        assert sheet[1][1] == {'one': 1.0, 'two': 2.0, 'three': 3.0}
        assert sheet[1][2] == {'one': u'wierd\\x97', 'two': u'char\\x98','three': u'set\\x99'}
