"""Video renderer module."""
from mfr.core import extension
from mfr.core.tasks import build_html

class MovieRenderer(extension.BaseRenderer):

    def render(self):
        content = '''
          <video width="320" height="240" controls>
              <source src="{file_path}">
              Your browser does not support the video tag.
              </video>
              '''.format(file_path=self.url)
        return content
        # return build_html(content, self.assets_url)

    @property
    def requires_file(self):
        return True