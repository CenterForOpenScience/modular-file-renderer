import os

import nbformat
import nbconvert
from traitlets.config import Config
from mako.lookup import TemplateLookup
from nbconvert.exporters import HTMLExporter

from mfr.core import extension
from mfr.extensions.ipynb import exceptions


class IpynbRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics.add('nbformat_version', nbformat.__version__)
        self.metrics.add('nbconvert_version', nbconvert.__version__)

    def render(self):
        try:
            with open(self.file_path, 'r') as file_pointer:
                notebook = nbformat.reads(file_pointer.read(), as_version=4)
        except ValueError as err:
            raise exceptions.InvalidFormatError('Could not read ipython notebook file. {}'.format(str(err)), str(self.metadata.download_url), err.__class__.__name__, str(err), self.__class__.__name__, self.metadata.ext)

        exporter = HTMLExporter(config=Config({
            'HTMLExporter': {
                'template_file': 'basic',
            },
            'CSSHtmlHeaderTransformer': {
                'enabled': False,
            },
        }))
        (body, _) = exporter.from_notebook_node(notebook)
        return self.TEMPLATE.render(base=self.assets_url, body=body)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
