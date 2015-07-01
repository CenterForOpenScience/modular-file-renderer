import os

from mfr.extensions.tabular.libs import xlrd_tools

BASE = os.path.dirname(os.path.abspath(__file__))


class TestTabularPandaTools:

    def test_xlsx_xlrd(self):
        with open(os.path.join(BASE, 'files', 'test.xlsx')) as fp:
            headers, data = xlrd_tools.xlsx_xlrd(fp)

        assert headers[0] == {'field': 'one', 'id': 'one', 'name': 'one', 'sortable': True}
        assert headers[1] == {'field': 'two', 'id': 'two', 'name': 'two', 'sortable': True}
        assert headers[2] == {'field': 'three', 'id': 'three', 'name': 'three', 'sortable': True}
        assert data[0] == {'one': 'a', 'two': 'b', 'three': 'c'}
        assert data[1] == {'one': 1.0, 'two': 2.0, 'three': 3.0}
        assert data[2] == {'one': u'wierd\\x97', 'two': u'char\\x98','three': u'set\\x99'}
