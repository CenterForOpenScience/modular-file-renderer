import os

import chardet
import pygments
import pygments.lexers
import pygments.lexers.special
import pygments.formatters
from pygments.util import ClassNotFound
from mako.lookup import TemplateLookup

from mfr.extensions.codepygments import settings
from mfr.core import extension, exceptions
from mfr.extensions.codepygments import exceptions as cp_exceptions


class CodePygmentsRenderer(extension.BaseRenderer):

    DEFAULT_LEXER = pygments.lexers.special.TextLexer

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics.add('pygments_version', pygments.__version__)

    def render(self):
        file_size = os.path.getsize(self.file_path)
        if file_size > settings.MAX_SIZE:
            raise(cp_exceptions.FileToLargeException('Text files larger than 64kb are not rendered; please download the file to view.'))
        with open(self.file_path, 'rb') as fp:
            body = self._render_html(fp, self.metadata.ext)
            return self.TEMPLATE.render(base=self.assets_url, body=body)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True

    def _render_html(self, fp, ext, *args, **kwargs):
        """Generate an html representation of the file
        :param fp: File pointer
        :param ext: File name extension
        :return: Content html
        """
        formatter = pygments.formatters.HtmlFormatter()
        data = fp.read()

        content, exception, encoding = None, None, 'utf-8'
        try:
            content = data.decode(encoding)
        except UnicodeDecodeError as e:
            exception = e

        if exception is not None:
            detected_encoding = chardet.detect(data)
            try:
                encoding = detected_encoding['encoding']
                content = data.decode(encoding)
            except KeyError:
                exception = exceptions.RendererError(
                    'Unable to detect encoding of source file', code=400)
            except UnicodeDecodeError as e:
                exception = e

        if content is None:
            assert exception is not None, 'Got no content or exception'
            if isinstance(exception, UnicodeDecodeError):
                exception = exceptions.RendererError('Unable to decode file as {}'.format(encoding), code=400)
            raise exception

        self.metrics.merge({'encoding': encoding, 'default_lexer': False})

        try:
            lexer = pygments.lexers.guess_lexer_for_filename(ext, content)
        except ClassNotFound:
            self.metrics.add('default_lexer', True)
            lexer = self.DEFAULT_LEXER()

        self.metrics.add('lexer', lexer.name)
        return pygments.highlight(content, lexer, formatter)
