"""Audio renderer module."""
from mfr.core import extension


class AudioRenderer(extension.BaseRenderer):

    def render(self):
        return '<audio controls>{file_name} <source src="{file_path}">'.format(
            file_name=self.file_path,
            file_path=self.url
        )

    @property
    def requires_file(self):
        return False