import os
from mfr.ext.tabular.libs import csv_tools

HERE = os.path.dirname(os.path.abspath(__file__))

def test_csv_csv_returns_headers_and_data():
    with open(os.path.join(HERE, 'fixtures', 'test.csv')) as fp:
        headers, data = csv_tools.csv_csv(fp)

    assert headers[0] == {'field': 'one', 'id': 'one', 'name': 'one'}
    assert data[0] == {'one': 'a', 'two': 'b', 'three': 'c'}
