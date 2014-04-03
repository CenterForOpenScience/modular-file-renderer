"""Project-wide test configuration, including fixutres that can be
used by any module.

Example test: ::

    def test_my_renderer(fakefile):
        assert my_renderer(fakefile) == '..expected result..'

"""
import io
import pytest

@pytest.fixture
def fakefile():
    return io.BytesIO(b'foo')
