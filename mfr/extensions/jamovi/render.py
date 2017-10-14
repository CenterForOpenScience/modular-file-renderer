
import os
from zipfile import ZipFile, BadZipFile
from distutils.version import LooseVersion

from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions.jamovi import exceptions as jamovi_exceptions
from mfr.extensions.jamovi.html_processor import HTMLProcessor


class JamoviRenderer(extension.BaseRenderer):

    # Minimum data archive version supported
    MINIMUM_VERSION = LooseVersion('1.0.2')

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    MESSAGE_FILE_CORRUPT = 'This jamovi file is corrupt and cannot be viewed.'
    MESSAGE_NO_PREVIEW = 'This jamovi file does not support previews.'

    def render(self):
        try:
            with ZipFile(self.file_path) as zip_file:
                self._check_file(zip_file)
                body = self._render_html(zip_file, self.metadata.ext)
                return self.TEMPLATE.render(base=self.assets_url, body=body)
        except BadZipFile as err:
            raise jamovi_exceptions.JamoviRendererError(
                '{} {}.'.format(self.MESSAGE_FILE_CORRUPT, str(err)),
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
            raise jamovi_exceptions.JamoviRendererError(
                self.MESSAGE_NO_PREVIEW,
            )

        processor = HTMLProcessor(zip_file)
        processor.feed(index)

        return processor.final_html()

    def _check_file(self, zip_file):
        """Check if the file is OK (not corrupt)
        :param zip_file: an opened ZipFile representing the jamovi file
        :return: True
        """
        # Extract manifest file content
        try:
            with zip_file.open('META-INF/MANIFEST.MF') as manifest_data:
                manifest = manifest_data.read().decode('utf-8')
        except KeyError:
            raise jamovi_exceptions.JamoviFileCorruptError(
                '{} Missing META-INF/MANIFEST.MF'.format(self.MESSAGE_FILE_CORRUPT),
                extension=self.metadata.ext,
                corruption_type='key_error',
                reason='zip missing ./META-INF/MANIFEST.MF',
            )

        lines = manifest.split('\n')

        # Search for Data-Archive-Version
        dataArchiveVersionStr = None
        for line in lines:
            keyValue = line.split(':')
            if len(keyValue) == 2:
                key = keyValue[0].strip()
                value = keyValue[1].strip()
                if key == 'Data-Archive-Version':
                    dataArchiveVersionStr = value
                    break
        else:
            raise jamovi_exceptions.JamoviFileCorruptError(
                '{} Data-Archive-Version not found.'.format(self.MESSAGE_FILE_CORRUPT),
                extension=self.metadata.ext,
                corruption_type='manifest_parse_error',
                reason='Data-Archive-Version not found.',
            )

        # Check that the file is new enough (contains preview content)
        dataArchiveVersion = LooseVersion(dataArchiveVersionStr)
        try:
            if dataArchiveVersion < self.MINIMUM_VERSION:
                raise jamovi_exceptions.JamoviFileCorruptError(
                    '{} Data-Archive-Version is too old.'.format(self.MESSAGE_FILE_CORRUPT),
                    extension=self.metadata.ext,
                    corruption_type='manifest_parse_error',
                    reason='Data-Archive-Version not found.',
                )
        except TypeError:
            raise jamovi_exceptions.JamoviFileCorruptError(
                '{} Data-Archive-Version not parsable.'.format(self.MESSAGE_FILE_CORRUPT),
                extension=self.metadata.ext,
                corruption_type='manifest_parse_error',
                reason='Data-Archive-Version ({}) not parsable.'.format(dataArchiveVersionStr),
            )

        return True
