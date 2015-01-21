import os

from ..libs import xlrd_tools

HERE = os.path.dirname(os.path.abspath(__file__))

def test_xlsx_xlrd():
    with open(os.path.join(HERE, 'fixtures', 'test.xlsx')) as fp:
        headers, data = xlrd_tools.xlsx_xlrd(fp)

    assert headers[0] == {'field': 'one', 'id': 'one', 'name': 'one'}
    assert data[0] == {'one': 'a', 'two': 'b', 'three': 'c'}
