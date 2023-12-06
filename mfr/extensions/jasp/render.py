import os

from mako.lookup import TemplateLookup
from mfr.core import extension
from mfr.extensions.jasp import exceptions
from zipfile import ZipFile, BadZipFile
from .html_processor import HTMLProcessor

class JASPRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    MESSAGE_FILE_CORRUPT = 'This JASP file is corrupt and cannot be viewed.'

    def render(self):
        try:
            with ZipFile(self.file_path) as zip_file:
                body = self._render_html(zip_file, self.metadata.ext)
                return self.TEMPLATE.render(base=self.assets_url, body=body)
        except BadZipFile as err:
            raise exceptions.JaspFileCorruptError(
                '{} Failure to unzip. {}.'.format(self.MESSAGE_FILE_CORRUPT, str(err)),
                extension=self.metadata.ext,
                corruption_type='bad_zip',
                reason=str(err),
            )

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True

    def _render_html(self, zip_file, ext, *args, **kwargs):
        index = None
        try:
            with zip_file.open('index.html') as index_data:
                index = index_data.read().decode('utf-8')
        except KeyError:
            raise exceptions.JaspFileCorruptError(
                '{} Missing index.html.'.format(self.MESSAGE_FILE_CORRUPT),
                extension=self.metadata.ext,
                corruption_type='key_error',
                reason='jasp missing ./index.html',
            )

        processor = HTMLProcessor(zip_file)
        processor.feed(index)

        return processor.final_html()
