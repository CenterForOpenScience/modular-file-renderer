import os

from mako.lookup import TemplateLookup
from mfr.core import extension
from mfr.extensions.jasp import exceptions
from zipfile import ZipFile, BadZipFile
from distutils.version import LooseVersion

from .html_processor import HTMLProcessor

class JASPRenderer(extension.BaseRenderer):

    # Minimum data archive version supported
    MINIMUM_VERSION = LooseVersion('1.0.2')

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    MESSAGE_FILE_CORRUPT = 'This JASP file is corrupt, and cannot be viewed.'

    def render(self):
        try:
            with ZipFile(self.file_path) as zip_file:
                self._check_file(zip_file)
                body = self._render_html(zip_file, self.metadata.ext)
                return self.TEMPLATE.render(base=self.assets_url, body=body)
        except BadZipFile as err:
            raise exceptions.JaspFileCorruptError('{} Failure to unzip. {}.'.format(self.MESSAGE_FILE_CORRUPT, str(err)), 'bad_zip', str(err), self.__class__.__name__, self.metadata.ext)

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
            raise exceptions.JaspFileCorruptError('{} Missing index.html.'.format(self.MESSAGE_FILE_CORRUPT), 'key_error', 'zip missing ./index.html', self.__class__.__name__, self.metadata.ext)

        processor = HTMLProcessor(zip_file)
        processor.feed(index)

        return processor.final_html()

    def _check_file(self, zip_file):
        """Check if the file is OK (not corrupt)
        :param zip_file: an opened ZipFile representing the JASP file
        :return: True
        """
        # Extract manifest file content
        try:
            with zip_file.open('META-INF/MANIFEST.MF') as manifest_data:
                manifest = manifest_data.read().decode('utf-8')
        except KeyError:
            raise exceptions.JaspFileCorruptError('{} Missing META-INF/MANIFEST.MF'.format(self.MESSAGE_FILE_CORRUPT), 'key_error', 'zip missing ./META-INF/MANIFEST.MF', self.__class__.__name__, self.metadata.ext)

        lines = manifest.split('\n')

        # Search for Data-Archive-Version
        dataArchiveVersion, createdBy = None, ''
        for line in lines:
            keyValue = line.split(':')
            if len(keyValue) == 2:
                key = keyValue[0].strip()
                value = keyValue[1].strip()
                if key == 'Data-Archive-Version':
                    dataArchiveVersion = value
                elif key == 'Created-By':
                    createdBy = str(value)
        if not dataArchiveVersion:
            raise exceptions.JaspFileCorruptError('{} Data-Archive-Version not found.'.format(self.MESSAGE_FILE_CORRUPT), 'manifest_parse_error', 'Data-Archive-Version not found.', self.__class__.__name__, self.metadata.ext)

        try:
            dataArchiveVersion = LooseVersion(dataArchiveVersion)
        except ValueError:
            raise exceptions.JaspFileCorruptError('{} Data-Archive-Version not parsable.'.format(self.MESSAGE_FILE_CORRUPT), 'manifest_parse_error', 'Data-Archive-Version not parsable.', self.__class__.__name__, self.metadata.ext)

        # Check that the file is new enough (contains preview content)
        if dataArchiveVersion < self.MINIMUM_VERSION:
            minimum_version = self.MINIMUM_VERSION.vstring
            data_archive_version = dataArchiveVersion.vstring
            raise exceptions.JaspVersionError('This JASP file was created with an older data archive version({}), and cannot be previewed. Minimum data archive version is {}.'.format(data_archive_version, minimum_version), createdBy, data_archive_version, minimum_version, self.__class__.__name__, self.metadata.ext)

        return True
