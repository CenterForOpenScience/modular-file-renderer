from mfr.core import FileHandler, get_file_extension
from mfr_audio.render import render_audio_tag

# TODO(asmacdo) full list of audio files
EXTENSIONS = [
    '.mp3',
    '.ogg',
    '.wav',
]


class Handler(FileHandler):
    """The audio file handler."""

    renderers = {
        'html': render_audio_tag,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
