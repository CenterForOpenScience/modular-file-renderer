import os

import pytest

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
        assert sheet[1][2] == {'one': u'wierd\\x97', 'two': u'char\\x98', 'three': u'set\\x99'}

    def test_xlsx_xlrd_duplicate_fields(self):
        with open(os.path.join(BASE, 'files', 'test_duplicate.xlsx')) as fp:
            sheets = xlrd_tools.xlsx_xlrd(fp)

        sheet = sheets.popitem()[1]
        assert sheet[0][0] == {'id': 'Name', 'name': 'Name', 'field': 'Name', 'sortable': True}
        assert sheet[0][1] == {'id': 'Dup (1)', 'name': 'Dup (1)',
                                'field': 'Dup (1)', 'sortable': True}
        assert sheet[0][2] == {'id': 'Dup (2)', 'name': 'Dup (2)',
                                'field': 'Dup (2)', 'sortable': True}
        assert sheet[0][3] == {'id': 'Dup (3)', 'name': 'Dup (3)',
                                'field': 'Dup (3)', 'sortable': True}
        assert sheet[0][4] == {'id': 'Dup (4)', 'name': 'Dup (4)',
                                'field': 'Dup (4)', 'sortable': True}
        assert sheet[0][5] == {'id': 'Not Dup', 'name': 'Not Dup',
                                'field': 'Not Dup', 'sortable': True}
        assert sheet[1][0] == {'Name': 1.0, 'Dup (1)': 2.0, 'Dup (2)': 3.0,
                            'Dup (3)': 4.0, 'Dup (4)': 5.0, 'Not Dup': 6.0}

    def test_xlsx_xlrd_duplicate_fields_handle_naming(self):
        with open(os.path.join(BASE, 'files', 'test_duplicate_uuid.xlsx')) as fp:
            sheets = xlrd_tools.xlsx_xlrd(fp, max_iterations=10)

        sheet = sheets.popitem()[1]

        # this if you raise max iterations, it will be named dup (13) instead of dup (<uuid>)
        assert sheet[0][1]['field'] != 'dup (13)'
        # using `len` is an easy way to see the uuid has been appended
        assert len(sheet[0][1]['field']) > 24
