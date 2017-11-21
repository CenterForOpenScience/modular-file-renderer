import os
import shutil

from mako.lookup import TemplateLookup

from mfr.core import utils
from mfr.core import extension
from mfr.extensions import settings as ext_settings
from mfr.extensions.papaya import settings as papaya_settings


class PapayaRenderer(extension.BaseRenderer):

    data_dir = papaya_settings.DATA_DIR
    data_ttl = papaya_settings.DATA_TTL
    comp_ext = ext_settings.COMPRESSED_EXT

    TEMPLATE = TemplateLookup(
        directories=[
            os.path.join(os.path.dirname(__file__), 'templates')
        ]).get_template('viewer.mako')

    def render(self):
        self.remove_old_files()
        file_name = os.path.basename(self.file_path)
        file_ext = utils.get_full_file_ext(self.metadata.ext, self.metadata.name)
        file_name = file_name + file_ext
        shutil.copyfile(self.file_path, self.data_dir + file_name)
        return self.TEMPLATE.render(base=self.assets_url, file_name=file_name)

    def remove_old_files(self):

        for data_file in os.listdir(self.data_dir):
            if utils.file_expired(self.data_dir + data_file, self.data_ttl):
                os.unlink(self.data_dir + data_file)

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
