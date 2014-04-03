"""Project-wide test configuration, including fixutres that can be
used by any module.

Example test: ::

    def test_my_renderer(fakefile):
        assert my_renderer(fakefile) == '..expected result..'

"""
import pytest
import mock

@pytest.fixture
def fakefile():
    """A simple file-like object."""
    return mock.Mock(spec=file)
