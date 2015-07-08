import pydocx.export
from mako.lookup import TemplateLookup

from mfr.core import extension, TEMPLATE_BASE


class DocxRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            TEMPLATE_BASE
        ]).get_template('docx_viewer.mako')

    # Workaround to remove default stylesheet and inlined styles
    # see: https://github.com/CenterForOpenScience/pydocx/issues/102
    class _PyDocXHTMLExporter(pydocx.export.PyDocXHTMLExporter):

        def style(self):
            return ''

        def indent(self, text, *args, **kwargs):
            return text

    def render(self):
        body = self._PyDocXHTMLExporter(self.file_path).parsed
        return self.TEMPLATE.render(base=self.assets_url, body=body, md5=self.extra.get('md5'))

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
