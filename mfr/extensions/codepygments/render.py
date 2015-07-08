import pygments.lexers
import pygments.lexers.special
import pygments.formatters
from pygments.util import ClassNotFound
from mako.lookup import TemplateLookup

from mfr.core import extension, TEMPLATE_BASE


class CodePygmentsRenderer(extension.BaseRenderer):

    DEFAULT_LEXER = pygments.lexers.special.TextLexer

    TEMPLATE = TemplateLookup(
        directories=[
            TEMPLATE_BASE
        ]).get_template('codepygments_viewer.mako')

    def render(self):
        with open(self.file_path, 'rb') as fp:
            body = self._render_html(fp, self.metadata.ext)
            return self.TEMPLATE.render(base=self.assets_url, body=body, md5=self.extra.get('md5'))

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True

    def _render_html(self, fp, ext, *args, **kwargs):
        """Generate an html representation of the file
        :param fp: File pointer
        :return: Content html
        """
        formatter = pygments.formatters.HtmlFormatter()
        data = fp.read()

        content, exception = None, None
        for encoding in ['windows-1252', 'utf-8', 'utf-16', 'ISO-8859-2']:
            try:
                content = data.decode(encoding)
                break
            except UnicodeDecodeError as e:
                exception = e
        if content is None:
            assert exception is not None, 'Got not content or exception'
            raise exception

        try:
            lexer = pygments.lexers.guess_lexer_for_filename(ext, content)
        except ClassNotFound:
            lexer = self.DEFAULT_LEXER()
        return pygments.highlight(content, lexer, formatter)
