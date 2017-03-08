import os
import zipfile

from mako.lookup import TemplateLookup

from mfr.core import extension


class ZipRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        zip_file = zipfile.ZipFile(self.file_path, 'r')

        return self.TEMPLATE.render(zipped_filenames=self.format_zip(zip_file))

    def format_zip(self, zip_file):
        return '<br>'.join(zip_file.namelist())

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
