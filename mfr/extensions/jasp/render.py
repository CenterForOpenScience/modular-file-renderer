import json
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

    MESSAGE_FILE_CORRUPT = 'This JASP file is corrupt and cannot be viewed.'

    def render(self):
        try:
            with ZipFile(self.file_path) as zip_file:
                self._check_file(zip_file)
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
                reason='zip missing ./index.html',
            )

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
            try:
                # new manifest location
                with zip_file.open('manifest.json') as manifest_data:
                    manifest, flavor = manifest_data.read().decode('utf-8'), 'json'
            except KeyError:
                # old manifest location
                with zip_file.open('META-INF/MANIFEST.MF') as manifest_data:
                    manifest, flavor = manifest_data.read().decode('utf-8'), 'java'
        except KeyError:
            raise exceptions.JaspFileCorruptError(
                '{} Missing manifest'.format(self.MESSAGE_FILE_CORRUPT),
                extension=self.metadata.ext,
                corruption_type='key_error',
                reason='zip missing manifest',
            )

        if flavor == 'java':
            self._verify_java_manifest(manifest)
        else:
            self._verify_json_manifest(manifest)

        return True

    def _verify_java_manifest(self, manifest):
        lines = manifest.split('\n')

        # Search for Data-Archive-Version
        dataArchiveVersionStr, createdBy = None, ''
        for line in lines:
            keyValue = line.split(':')
            if len(keyValue) == 2:
                key = keyValue[0].strip()
                value = keyValue[1].strip()
                if key == 'Data-Archive-Version':
                    dataArchiveVersionStr = value
                elif key == 'Created-By':
                    createdBy = str(value)
        if not dataArchiveVersionStr:
            raise exceptions.JaspFileCorruptError(
                '{} Data-Archive-Version not found.'.format(self.MESSAGE_FILE_CORRUPT),
                extension=self.metadata.ext,
                corruption_type='manifest_parse_error',
                reason='Data-Archive-Version not found.',
            )

        # Check that the file is new enough (contains preview content)
        dataArchiveVersion = LooseVersion(dataArchiveVersionStr)
        try:
            if dataArchiveVersion < self.MINIMUM_VERSION:
                minimum_version = self.MINIMUM_VERSION.vstring
                data_archive_version = dataArchiveVersion.vstring
                raise exceptions.JaspVersionError(
                    'This JASP file was created with an older data archive '
                    'version ({}) and cannot be previewed. Minimum data archive '
                    'version is {}.'.format(data_archive_version, minimum_version),
                    extension=self.metadata.ext,
                    created_by=createdBy,
                    actual_version=data_archive_version,
                    required_version=minimum_version,
                )
        except TypeError:
            raise exceptions.JaspFileCorruptError(
                '{} Data-Archive-Version not parsable.'.format(self.MESSAGE_FILE_CORRUPT),
                extension=self.metadata.ext,
                corruption_type='manifest_parse_error',
                reason='Data-Archive-Version ({}) not parsable.'.format(dataArchiveVersionStr),
            )

        return

    def _verify_json_manifest(self, manifest):

        manifest_data = json.loads(manifest)

        jasp_archive_version_str = manifest_data.get('jaspArchiveVersion', None)
        if not jasp_archive_version_str:
            raise exceptions.JaspFileCorruptError(
                '{} jaspArchiveVersion not found.'.format(self.MESSAGE_FILE_CORRUPT),
                extension=self.metadata.ext,
                corruption_type='manifest_parse_error',
                reason='jaspArchiveVersion not found.',
            )

        # Check that the file is new enough (contains preview content)
        jasp_archive_version = LooseVersion(jasp_archive_version_str)
        try:
            if jasp_archive_version < self.MINIMUM_VERSION:
                minimum_version = self.MINIMUM_VERSION.vstring
                data_archive_version = jasp_archive_version.vstring
                raise exceptions.JaspVersionError(
                    'This JASP file was created with an older data archive '
                    'version ({}) and cannot be previewed. Minimum data archive '
                    'version is {}.'.format(data_archive_version, minimum_version),
                    extension=self.metadata.ext,
                    actual_version=data_archive_version,
                    required_version=minimum_version,
                )
        except TypeError:
            raise exceptions.JaspFileCorruptError(
                '{} jaspArchiveVersion not parsable.'.format(self.MESSAGE_FILE_CORRUPT),
                extension=self.metadata.ext,
                corruption_type='manifest_parse_error',
                reason='jaspArchiveVersion ({}) not parsable.'.format(jasp_archive_version_str),
            )

        return
