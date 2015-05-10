"""Audio renderer module."""
from mfr.core import extension


class AudioRenderer(extension.BaseRenderer):

    def render(self):
        return '<audio controls>{file_name} <source src="{file_path}">'.format(
        file_path=self.file_path,
        file_name=self.url
        )