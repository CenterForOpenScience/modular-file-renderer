from mfr.extensions.tabular import utilities


class TestTabularUtilities:

    def test_header_population_returns_list_of_dicts(self):
        fake_headers = ['one', 'two', 'three']
        populated = utilities.header_population(fake_headers)
        assert type(populated) == list
        assert type(populated[0]) == dict
        assert len(populated) == 3

    def test_data_population_returns_list_of_dicts(self):
        fake_headers = ['one', 'two', 'three']
        fake_data = [['a', 'b', 'c'], ['1', '2', '3']]
        populated = utilities.data_population(fake_data, fake_headers)
        assert type(populated) == list
        assert type(populated[0]) == dict
        assert len(populated) == 2

    def test_data_population_without_headers(self):
        fake_data = [['one', 'two', 'three'], ['a', 'b', 'c'], ['1', '2', '3']]
        populated = utilities.data_population(fake_data)
        assert type(populated) == list
        assert type(populated[0]) == dict
        assert len(populated) == 3
