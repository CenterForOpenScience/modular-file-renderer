from mfr_tabular import csv_tools


def test_csv_csv_returns_headers_and_data():
    with open('mfr_tabular/tests/fixtures/test.csv') as fp:
        headers, data = csv_tools.csv_csv(fp)

    assert headers[0] == {'field': 'one', 'id': 'one', 'name': 'one'}
    assert data[0] == {'one': 'a', 'two': 'b', 'three': 'c'}
