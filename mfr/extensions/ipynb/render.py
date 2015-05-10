import os

from mfr.core import extension
from mako.lookup import TemplateLookup

from IPython import nbformat
from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter


class IpynbRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        try:
            with open(self.file_path, 'r') as file_pointer:
                notebook = nbformat.reads(file_pointer.read(), as_version=4)
        except ValueError as e:
            # TODO: Generate application specific exception
            raise Exception('Invalid json: {}'.format(e))

        exporter = HTMLExporter(config=Config({
            'HTMLExporter': {
                'template_file': 'basic',
            },
            'CSSHtmlHeaderTransformer': {
                'enabled': False,
            },
        }))
        (body, _) = exporter.from_notebook_node(notebook)
        return self.TEMPLATE.render(body=body, base=self.assets_url)

    @property
    def requires_file(self):
        return True
