import os

from mako.lookup import TemplateLookup
from mfr.core import extension
from mfr.core.exceptions import RendererError
from zipfile import ZipFile, BadZipFile
from distutils.version import LooseVersion

from .html_processor import HTMLProcessor

class JASPRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    MESSAGE_FILE_CORRUPT = "This JASP file is corrupt, and cannot be viewed"
    MESSAGE_FILE_TO_OLD = "This JASP file was created in an early version of JASP, and cannot be previewed"

    def render(self):
        try:
            with ZipFile(self.file_path) as zip_file:
                self._check_file(zip_file)
                body = self._render_html(zip_file, self.metadata.ext)
                return self.TEMPLATE.render(base=self.assets_url, body=body)
        except BadZipFile:
            raise RendererError(self.MESSAGE_FILE_CORRUPT)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True

    def _render_html(self, zip_file, ext, *args, **kwargs):

        index = None

        try:
            with zip_file.open("index.html") as index_data:
                index = index_data.read().decode("utf-8")

        except KeyError:
            raise RendererError(self.MESSAGE_FILE_CORRUPT)

        processor = HTMLProcessor()
        processor.set_src_source(zip_file)
        processor.feed(index)

        return processor.final_html()

    def _check_file(self, zip_file):
        
        # Extract manifest file content

        try:
            with zip_file.open("META-INF/MANIFEST.MF") as manifest_data:
                manifest = manifest_data.read().decode("utf-8")
        except KeyError:
            raise RendererError(self.MESSAGE_FILE_CORRUPT)

        lines = manifest.split("\n")

        # Search for Data-Archive-Version

        for line in lines:
            keyValue = line.split(":")
            if len(keyValue) == 2:
                key = keyValue[0].strip()
                value = keyValue[1].strip()

                if key == "Data-Archive-Version":
                    dataArchiveVersion = value
                    break
        else:
            raise RendererError(self.MESSAGE_FILE_CORRUPT)

        try: 
            dataArchiveVersion = LooseVersion(dataArchiveVersion)
        except ValueError:
            raise RendererError(self.MESSAGE_FILE_CORRUPT)

        # Check that the file is new enough (contains preview content)

        if dataArchiveVersion < LooseVersion("1.0.2"):
            raise RendererError(self.MESSAGE_FILE_TO_OLD)

        return True

