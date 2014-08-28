import pytest
import mfr_movie
from mfr_movie.render import render_movie_tag


@pytest.mark.parametrize('filename', [
    'movie.ogv',
    'movie.avi',
    'movie.mp4',
    'movie.wmv',
    'movie.webm',
])
def test_detect_movie_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_movie.Handler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'fail.jpg',
    'fail.',
    'fail.hello',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_movie.Handler()
    assert handler.detect(fakefile) is False


def test_render_movie_tag(fakefile):
    result = render_movie_tag(fakefile, src='/movie.avi')
    assert 'src="/movie.avi"' in result
