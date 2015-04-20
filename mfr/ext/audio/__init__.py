from mfr.core_methods import FileHandler, get_file_extension
from .render import render_audio_tag

EXTENSIONS = [
    '.mp3',
    '.ogg',
    '.wav',
]


class Handler(FileHandler):
    """FileHandler for audio files."""

    renderers = {
        'html': render_audio_tag,
    }

    def detect(self, fp):
        return get_file_extension(fp.name) in EXTENSIONS
