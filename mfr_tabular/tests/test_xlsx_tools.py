from mfr_tabular.libs import xlrd_tools


def test_xlsx_xlrd():
    with open('mfr_tabular/tests/fixtures/test.xlsx') as fp:
        headers, data = xlrd_tools.xlsx_xlrd(fp)

    assert headers[0] == {'field': 'one', 'id': 'one', 'name': 'one'}
    assert data[0] == {'one': 'a', 'two': 'b', 'three': 'c'}
