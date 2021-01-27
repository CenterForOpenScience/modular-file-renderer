import logging
from io import StringIO
from random import choice
from string import ascii_letters

import pytest

from mfr.extensions.tabular.exceptions import TabularRendererError
from mfr.extensions.tabular.libs.stdlib_tools import _find_new_line, _trim_or_append_data

logger = logging.getLogger(__name__)

INIT_SNIFF_SIZE = 128
MAX_RENDER_SIZE = INIT_SNIFF_SIZE * 8


@pytest.fixture
def text_with_lf():
    return 'text_with_lf\nanother_row\na_third_row'


@pytest.fixture
def text_with_cr():
    return 'text_with_cr\ranother_row\ra_third_row'


@pytest.fixture
def text_with_cr_lf():
    return 'text_with_cr_lf\r\nanother_row\r\na_third_row'


@pytest.fixture
def text_without_new_line():
    return 'text_without_new_line\tthe_same_row\tthe_same_row_continued'


@pytest.fixture
def small_text_partial():
    return ''.join(choice(ascii_letters) for _ in range(INIT_SNIFF_SIZE - 2))


@pytest.fixture
def fp_small(small_text_partial):
    return StringIO('{}\nanother_row\n'.format(small_text_partial))


@pytest.fixture
def large_text_partial():
    return ''.join(choice(ascii_letters) for _ in range(MAX_RENDER_SIZE - INIT_SNIFF_SIZE))


@pytest.fixture
def fp_large(large_text_partial):
    return StringIO('{}\nanother_row\n'.format(large_text_partial))


@pytest.fixture
def fp_empty():
    return StringIO('')


@pytest.fixture
def one_line_text():
    return ''.join(choice(ascii_letters) for _ in range(MAX_RENDER_SIZE - INIT_SNIFF_SIZE))


@pytest.fixture
def fp_one_line(one_line_text):
    return StringIO(one_line_text)


@pytest.fixture
def fp_oversize():
    oversize_text_partial = ''.join(choice(ascii_letters) for _ in range(MAX_RENDER_SIZE + 2))
    return StringIO('{}the_same_row\nanother_row\n'.format(oversize_text_partial))


class TestFindNewLine:

    def test_find_new_line_lf(self, text_with_lf):
        index = _find_new_line(text_with_lf)
        assert index == 12

    def test_find_new_line_cr(self, text_with_cr):
        index = _find_new_line(text_with_cr)
        assert index == 12

    def test_find_new_line_cr_lf(self, text_with_cr_lf):
        index = _find_new_line(text_with_cr_lf)
        assert index == 15

    def test_find_new_line_none(self, text_without_new_line):
        index = _find_new_line(text_without_new_line)
        assert index == -1


class TestTrimORAppendData:

    def test_trim_or_append_data_small(self, fp_small, small_text_partial):
        data = fp_small.read(INIT_SNIFF_SIZE)
        data = _trim_or_append_data(fp_small, data, INIT_SNIFF_SIZE, 0,
                                    max_render_size=MAX_RENDER_SIZE)
        fp_small.close()
        assert data == small_text_partial

    def test_trim_or_append_data_large(self, fp_large, large_text_partial):
        data = fp_large.read(INIT_SNIFF_SIZE)
        data = _trim_or_append_data(fp_large, data, INIT_SNIFF_SIZE, 0,
                                    max_render_size=MAX_RENDER_SIZE)
        fp_large.close()
        assert data == large_text_partial

    def test_trim_or_append_data_empty(self, fp_empty):
        data = fp_empty.read(INIT_SNIFF_SIZE)
        data = _trim_or_append_data(fp_empty, data, INIT_SNIFF_SIZE, 0,
                                    max_render_size=MAX_RENDER_SIZE)
        fp_empty.close()
        assert data == ''

    def test_trim_or_append_data_one_line(self, fp_one_line, one_line_text):
        data = fp_one_line.read(INIT_SNIFF_SIZE)
        data = _trim_or_append_data(fp_one_line, data, INIT_SNIFF_SIZE, 0,
                                    max_render_size=MAX_RENDER_SIZE)
        fp_one_line.close()
        assert data == one_line_text

    def test_trim_or_append_data_error_upon_max_render_size(self, fp_oversize):
        with pytest.raises(TabularRendererError):
            data = fp_oversize.read(INIT_SNIFF_SIZE)
            _trim_or_append_data(fp_oversize, data, INIT_SNIFF_SIZE, 0,
                                 max_render_size=MAX_RENDER_SIZE)
        fp_oversize.close()
