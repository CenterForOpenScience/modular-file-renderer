import os

import pydocx.export
from mako.lookup import TemplateLookup

from mfr.core import extension


class DocxRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    # Workaround to remove default stylesheet and inlined styles
    # see: https://github.com/CenterForOpenScience/pydocx/issues/102
    class _PyDocXHTMLExporter(pydocx.export.PyDocXHTMLExporter):

        def style(self):
            return ''

        def indent(self, text, *args, **kwargs):
            return text

    def render(self):
        body = self._PyDocXHTMLExporter(self.file_path).parsed
        return self.TEMPLATE.render(base=self.assets_url, body=body, md5 = self.extra.get('md5'))

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
