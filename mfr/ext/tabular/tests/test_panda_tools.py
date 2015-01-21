from mfr_tabular.libs import panda_tools


def test_data_from_dateframe():
    with open('mfr_tabular/tests/fixtures/test.csv') as fp:
        headers, data = panda_tools.csv_pandas(fp)

    assert type(data) == list
    assert type(data[0]) == dict


def test_csv_pandas():
    with open('mfr_tabular/tests/fixtures/test.csv') as fp:
        headers, data = panda_tools.csv_pandas(fp)

    assert headers[0] == {'field': 'one', 'id': 'one', 'name': 'one'}
    assert data[0] == {'one': 'a', 'two': 'b', 'three': 'c'}


# def test_dta_pandas():
#     with open('mfr_tabular/tests/fixtures/test.dta') as fp:
#         headers, data = panda_tools.dta_pandas(fp)

#     assert headers[0] == {'field': 'one', 'id': 'one', 'name': 'one'}
#     assert data[0] == {'one': 'a', 'two': 'b', 'three': 'c'}

#     assert len(data) is 2
#     assert len(headers) is 3
