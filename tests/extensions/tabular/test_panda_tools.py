import os

from mfr.extensions.tabular.libs import panda_tools

BASE = os.path.dirname(os.path.abspath(__file__))


class TestTabularPandaTools:

    def test_data_from_dateframe(self):
        with open(os.path.join(BASE, 'files', 'test.csv')) as fp:
            headers, data = panda_tools.csv_pandas(fp)

        assert type(data) == list
        assert type(data[0]) == dict

    def test_csv_pandas(self):
        with open(os.path.join(BASE, 'files', 'test.csv')) as fp:
            headers, data = panda_tools.csv_pandas(fp)

        assert headers[0] == {'field': 'one', 'id': 'one', 'name': 'one', 'sortable': True}
        assert data[0] == {'one': 'à', 'two': 'b', 'three': 'c'}

    def test_tsv_pandas(self):
        with open(os.path.join(BASE, 'files', 'test.tsv')) as fp:
            headers, data = panda_tools.csv_pandas(fp)

        assert headers[0] == {'field': 'one\ttwo\tthree', 'id': 'one\ttwo\tthree', 'name': 'one\ttwo\tthree', 'sortable': True}
        assert data[0] == {'one\ttwo\tthree': 'a\tb\tc'}

    # def test_dta_pandas():
    #     with open('mfr_tabular/tests/fixtures/test.dta') as fp:
    #         headers, data = panda_tools.dta_pandas(fp)

    #     assert headers[0] == {'field': 'one', 'id': 'one', 'name': 'one'}
    #     assert data[0] == {'one': 'a', 'two': 'b', 'three': 'c'}
    #     assert len(data) is 2
    #     assert len(headers) is 3
