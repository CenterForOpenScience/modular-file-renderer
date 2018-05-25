import os

import chardet
from humanfriendly import format_size
import pygments
import pygments.lexers
import pygments.lexers.special
import pygments.formatters
from pygments.util import ClassNotFound
from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.codepygments import settings
from mfr.extensions.codepygments import exceptions


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
            raise exceptions.FileTooLargeError(
                'Text files larger than {} are not rendered. Please download '
                'the file to view.'.format(format_size(settings.MAX_SIZE, binary=True)),
                file_size=file_size,
                max_size=settings.MAX_SIZE,
                extension=self.metadata.ext,
            )

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

        content, encoding = None, 'utf-8'
        try:
            content = data.decode(encoding)
        except UnicodeDecodeError:
            detected_encoding = chardet.detect(data)
            encoding = detected_encoding.get('encoding', None)
            if encoding is None:
                raise exceptions.FileDecodingError(
                    message='Unable to detect encoding of source file.',
                    extension=ext,
                    category='undetectable_encoding',
                    code=400,
                )

            try:
                content = data.decode(encoding)
            except UnicodeDecodeError as err:
                raise exceptions.FileDecodingError(
                    message='Unable to decode file as {}.'.format(encoding),
                    extension=ext,
                    category='undecodable',
                    original_exception=err,
                    code=400,
                )

        if content is None:
            raise exceptions.FileDecodingError(
                message='File decoded to undefined using encoding "{}"'.format(encoding),
                extension=ext,
                category='decoded_to_undefined',
                code=500,
            )

        self.metrics.merge({'encoding': encoding, 'default_lexer': False})

        try:
            # check if there is a lexer available for more obscure file types
            if ext in settings.lexer_lib.keys():
                lexer = pygments.lexers.get_lexer_by_name(settings.lexer_lib[ext])
            else:
                lexer = pygments.lexers.guess_lexer_for_filename(ext, content)
        except ClassNotFound:
            self.metrics.add('default_lexer', True)
            lexer = self.DEFAULT_LEXER()

        self.metrics.add('lexer', lexer.name)
        return pygments.highlight(content, lexer, formatter)
