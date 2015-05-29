"""Video renderer module."""
from mfr.core import extension


class MovieRenderer(extension.BaseRenderer):

    def render(self):
        return '''
            <div class="embed-responsive embed-responsive-16by9">
                <video controls>
                  <source src="{}">
                  Your browser does not support the video tag.
                </video>
            </div>
            '''.format(self.url)

    @property
    def requires_file(self):
        return False
