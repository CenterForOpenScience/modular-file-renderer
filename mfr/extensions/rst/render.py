""" ReStructuredText renderer module """
from docutils.core import publish_parts
from mfr.core import extension

class RstRenderer(extension.BaseRenderer):

    def render(self):
        with open(self.file_path, 'r') as fp:
            return publish_parts(fp.read(), writer_name='html')['html_body']

    @property
    def requires_file(self):
        return False
