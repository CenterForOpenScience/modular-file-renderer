import pytest
import mfr_audio
import mfr
from mfr_audio.render import render_audio_tag


@pytest.mark.parametrize('filename', [
    'audio.mp3',
])
def test_detect_audio_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_audio.Handler()
    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'other.notaudio',
    'other.',
    'other',
    'othermp3',
])
def test_does_not_detect_other_extensions(fakefile, filename):
    fakefile.name = filename
    handler = mfr_audio.Handler()
    assert handler.detect(fakefile) is False


def test_render_audio_tag(fakefile):
    fakefile.name = "audio.mp3"
    result = render_audio_tag(fakefile)

    assert type(result) == mfr.core.RenderResult
    assert 'src="audio.mp3"' in result.content
