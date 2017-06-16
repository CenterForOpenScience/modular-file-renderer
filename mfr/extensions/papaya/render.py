import os
import time
import shutil

from mako.lookup import TemplateLookup

from mfr.core import extension
from mfr.extensions import settings as ext_settings
from mfr.extensions.papaya import settings


class PapayaRenderer(extension.BaseRenderer):

    data_dir = settings.DATA_DIR
    data_old = settings.DATA_OLD
    comp_ext = ext_settings.COMPRESSED_EXT

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        self.remove_old_files()
        file_name = os.path.basename(self.file_path)
        if self.metadata.ext in self.comp_ext.keys():
            second_ext = '.{}'.format(self.metadata.name.split('.')[-1])
            if second_ext in self.comp_ext[self.metadata.ext]:
                file_name = file_name + second_ext
        file_name = file_name + self.metadata.ext
        shutil.copyfile(self.file_path, self.data_dir + file_name)
        return self.TEMPLATE.render(base=self.assets_url, file_name=file_name)

    def remove_old_files(self):

        for data_file in os.listdir(self.data_dir):
            if data_file == '.gitignore':
                continue
            if (time.time() - os.path.getctime(self.data_dir + data_file)) >= self.data_old:
                os.unlink(self.data_dir + data_file)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
