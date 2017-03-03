import os
import io
import zipfile
import requests

from mako.lookup import TemplateLookup

from mfr.core import extension


class ZipRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):

        zip_file = self.fetch_zip()

        return self.TEMPLATE.render(zipped_filenames=self.format_zip(zip_file))

    def fetch_zip(self):
        r = requests.get(self.url)
        return zipfile.ZipFile(io.BytesIO(r.content))

    def format_zip(self, zip_file):
        return '<br>'.join(zip_file.namelist())

    @property
    def file_required(self):
        return False

    @property
    def cache_result(self):
        return False
