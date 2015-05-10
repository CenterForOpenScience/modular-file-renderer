"""Video renderer module."""
from mfr.core import extension

class MovieRenderer(extension.BaseRenderer):

    def render(self):
        content = '''
          <video width="320" height="240" controls>
              <source src="{file_path}">
              Your browser does not support the video tag.
              </video>
              '''.format(file_path=self.file_path)
        return content
