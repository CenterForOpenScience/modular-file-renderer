import os

import pytest

from mfr.extensions.tabular.libs import panda_tools

BASE = os.path.dirname(os.path.abspath(__file__))


class TestTabularPandaTools:

    def test_data_from_dateframe(self):
        with open(os.path.join(BASE, 'files', 'test.csv')) as fp:
            sheets = panda_tools.csv_pandas(fp)

        sheet = sheets.popitem()[1]
        assert type(sheet[0]) == list
        assert type(sheet[0][1]) == dict

    def test_csv_pandas(self):
        with open(os.path.join(BASE, 'files', 'test.csv')) as fp:
            sheets = panda_tools.csv_pandas(fp)

        sheet = sheets.popitem()[1]
        assert sheet[0][0] == {'field': 'one', 'id': 'one', 'name': 'one', 'sortable': True}
        assert sheet[1][0] == {'one': 'à', 'two': 'b', 'three': 'c'}

    def test_tsv_pandas(self):
        with open(os.path.join(BASE, 'files', 'test.tsv')) as fp:
            sheets = panda_tools.csv_pandas(fp)

        sheet = sheets.popitem()[1]
        assert sheet[0][0] == {'field': 'one\ttwo\tthree', 'id': 'one\ttwo\tthree', 'name': 'one\ttwo\tthree', 'sortable': True}
        assert sheet[1][0] == {'one\ttwo\tthree': 'a\tb\tc'}

    def test_invalid_dta(self):
        with open(os.path.join(BASE, 'files', 'invalid.dta')) as fp:
            with pytest.raises(ValueError):
                panda_tools.dta_pandas(fp)

    def test_dta_pandas(self):
        with open(os.path.join(BASE, 'files', 'test.dta')) as fp:
            sheets = panda_tools.dta_pandas(fp)

        sheet = sheets.popitem()[1]
        assert sheet == ([{'id': 'Actor', 'name': 'Actor', 'field': 'Actor', 'sortable': True},
            {'id': 'IMDBscore', 'name': 'IMDBscore', 'field': 'IMDBscore', 'sortable': True}],
            [{'Actor': '1', 'IMDBscore': 6.6}, {'Actor': '1', 'IMDBscore': 6.5},
            {'Actor': '1', 'IMDBscore': 7.3}, {'Actor': '1', 'IMDBscore': 7.8},
            {'Actor': '1', 'IMDBscore': 6.3}, {'Actor': '1', 'IMDBscore': 6.6},
            {'Actor': '1', 'IMDBscore': 6.1}, {'Actor': '1', 'IMDBscore': 7.1},
            {'Actor': '1', 'IMDBscore': 5.7}, {'Actor': '1', 'IMDBscore': 5.7},
            {'Actor': '1', 'IMDBscore': 7.1}, {'Actor': '1', 'IMDBscore': 7.6},
            {'Actor': '1', 'IMDBscore': 7.1}, {'Actor': '1', 'IMDBscore': 3.8},
            {'Actor': '1', 'IMDBscore': 8.0}, {'Actor': '1', 'IMDBscore': 4.7},
            {'Actor': '1', 'IMDBscore': 6.5}, {'Actor': '1', 'IMDBscore': 7.6},
            {'Actor': '1', 'IMDBscore': 6.3}, {'Actor': '1', 'IMDBscore': 5.4},
            {'Actor': '2', 'IMDBscore': 7.1}, {'Actor': '2', 'IMDBscore': 7.3},
            {'Actor': '2', 'IMDBscore': 6.2}, {'Actor': '2', 'IMDBscore': 7.4},
            {'Actor': '2', 'IMDBscore': 7.5}, {'Actor': '2', 'IMDBscore': 6.7},
            {'Actor': '2', 'IMDBscore': 6.2}, {'Actor': '2', 'IMDBscore': 4.7},
            {'Actor': '2', 'IMDBscore': 6.5}, {'Actor': '2', 'IMDBscore': 5.5},
            {'Actor': '2', 'IMDBscore': 5.4}, {'Actor': '2', 'IMDBscore': 7.7},
            {'Actor': '2', 'IMDBscore': 7.1}, {'Actor': '2', 'IMDBscore': 6.1},
            {'Actor': '2', 'IMDBscore': 6.7}, {'Actor': '2', 'IMDBscore': 7.0},
            {'Actor': '2', 'IMDBscore': 5.8}, {'Actor': '2', 'IMDBscore': 4.1},
            {'Actor': '2', 'IMDBscore': 5.7}, {'Actor': '2', 'IMDBscore': 6.1}])
