import os

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

    # def test_dta_pandas():
    #     with open('mfr_tabular/tests/fixtures/test.dta') as fp:
    #         headers, data = panda_tools.dta_pandas(fp)

    #     assert headers[0] == {'field': 'one', 'id': 'one', 'name': 'one'}
    #     assert data[0] == {'one': 'a', 'two': 'b', 'three': 'c'}
    #     assert len(data) is 2
    #     assert len(headers) is 3
