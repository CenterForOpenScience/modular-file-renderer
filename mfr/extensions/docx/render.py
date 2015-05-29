"""Docx renderer module."""
import pydocx.export

from mfr.core import extension


class DocxRenderer(extension.BaseRenderer):

    # Workaround to remove default stylesheet and inlined styles
    # see: https://github.com/CenterForOpenScience/pydocx/issues/102
    class _PyDocXHTMLExporter(pydocx.export.PyDocXHTMLExporter):

        def style(self):
            return ''

        def indent(self, text, *args, **kwargs):
            return text

    def render(self):
        return self._PyDocXHTMLExporter(self.file_path).parsed

    @property
    def requires_file(self):
        return True
