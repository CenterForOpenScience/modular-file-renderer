"""Audio renderer module."""
from mfr.core import extension


class AudioRenderer(extension.BaseRenderer):

    def render(self):
        return '''
            <audio controls>
              <source src="{}">
              Your browser does not support the audio tag.
            </audio>
            '''.format(self.url)

    @property
    def requires_file(self):
        return False
