import os
from http import HTTPStatus
from collections import OrderedDict

import pytest

from mfr.extensions.tabular.libs import stdlib_tools
from mfr.extensions.tabular.exceptions import(EmptyTableError,
                                              TabularRendererError)

BASE = os.path.dirname(os.path.abspath(__file__))


class TestTabularStdlibTools:

    def test_csv_stdlib(self):
        with open(os.path.join(BASE, 'files', 'test.csv')) as fp:
            sheets = stdlib_tools.csv_stdlib(fp)

        sheet = sheets.popitem()[1]
        assert sheet[0] == [
            {'id': 'one', 'field': 'one', 'name': 'one', 'sortable': True},
            {'id': 'two', 'field': 'two', 'name': 'two', 'sortable': True},
            {'id': 'three', 'field': 'three', 'name': 'three', 'sortable': True}
        ]
        assert sheet[1][0] == OrderedDict([('one', 'à'), ('two', 'b'), ('three', 'c')])
        assert sheet[1][1] == OrderedDict([('one', '1'), ('two', '2'), ('three', '3')])

    def test_tsv_stdlib(self):
        with open(os.path.join(BASE, 'files', 'test.tsv')) as fp:
            sheets = stdlib_tools.tsv_stdlib(fp)

        sheet = sheets.popitem()[1]
        assert sheet[0] == [
            {'id': 'one', 'field': 'one', 'name': 'one', 'sortable': True},
            {'id': 'two', 'field': 'two', 'name': 'two', 'sortable': True},
            {'id': 'three', 'field': 'three', 'name': 'three', 'sortable': True}
        ]
        assert sheet[1][0] == OrderedDict([('one', 'a'), ('two', 'b'), ('three', 'c')])
        assert sheet[1][1] == OrderedDict([('one', '1'), ('two', '2'), ('three', '3')])

    def test_tsv_stdlib_exception_raises(self):
        with open(os.path.join(BASE, 'files', 'invalid.tsv')) as fp:
            with pytest.raises(EmptyTableError) as e:
                stdlib_tools.tsv_stdlib(fp)
                assert e.value.code == HTTPStatus.BAD_REQUEST

    def test_csv_stdlib_exception_raises(self):
        with open(os.path.join(BASE, 'files', 'invalid.csv')) as fp:
            with pytest.raises(EmptyTableError) as e:
                stdlib_tools.tsv_stdlib(fp)
                assert e.value.code == HTTPStatus.BAD_REQUEST

    def test_csv_stdlib_other_exception_raises(self):
        with open(os.path.join(BASE, 'files', 'invalid_null.csv')) as fp:
            with pytest.raises(TabularRendererError) as e:
                stdlib_tools.tsv_stdlib(fp)
                assert e.value.code == HTTPStatus.BAD_REQUEST
