import os
import zipfile

import markupsafe
from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.core.utils import sizeof_fmt


class ZipRenderer(extension.BaseRenderer):

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        zip_file = zipfile.ZipFile(self.file_path, 'r')

        filelist = [{'name': markupsafe.escape(file.filename),
                     'size': sizeof_fmt(int(file.file_size)),
                     'date': "%d-%02d-%02d %02d:%02d:%02d" % file.date_time[:6]} for file in zip_file.filelist
                    if not file.filename.startswith('__MACOSX')]

        message = '' if filelist else 'This zip file is empty.'

        return self.TEMPLATE.render(zipped_filenames=filelist, message=message)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
