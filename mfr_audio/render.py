"""Audio renderer module."""
from mfr.core import RenderResult


def render_audio_tag(fp, src=None):
    """Create a simple audio tag for a static audio file"""

    src = src or fp.name

    content = '<audio controls>{file_name} <source src="{file_path}">'.format(
        file_path=src,
        file_name=fp.name
    )

    return RenderResult(content)
