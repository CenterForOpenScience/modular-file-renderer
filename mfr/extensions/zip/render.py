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

        return self.TEMPLATE.render(zipped_filenames=self.format_zip(zip_file))

    def format_zip(self, zip_file):

        if type(zip_file) != zipfile.ZipFile:
            return 'This is not a valid zip file.'

        filelist = [file for file in zip_file.filelist if not file.filename.startswith('__MACOSX')]

        if not filelist:
            return 'This zip file is empty.'

        message = '<table class="table table-hover">' \
                  '<thead>' \
                    '<th>%-46s</th><th>%19s</th><th>%12s</th>' \
                  '</thead>'\
                  % ('File Name', 'Modified    ', 'Size')

        for zinfo in filelist:
            date = "%d-%02d-%02d %02d:%02d:%02d" % zinfo.date_time[:6]
            message += "<tr><td>%-46s</td> <td>%s</td> <td>%s<td></tr>" %\
                       (markupsafe.escape(zinfo.filename), date, sizeof_fmt(int(zinfo.file_size)))

        message += '</table>'
        return message

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
