import pytest
import mfr
from mfr.extensions.audio import AudioRenderer

@pytest.mark.parametrize('filename', [
    'audio.mp3',
])
def test_detect_audio_extensions(fakefile, filename):
    fakefile.name = filename

    assert handler.detect(fakefile) is True


@pytest.mark.parametrize('filename', [
    'other.notaudio',
    'other.',
    'other',
    'othermp3',
])

def test_render_audio_tag(fakefile):
    fakefile.name = "audio.mp3"

    assert type(result) == mfr.core.RenderResult
    assert 'src="audio.mp3"' in result.content
