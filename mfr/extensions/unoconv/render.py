import os
import shutil
import subprocess

from mfr.core import utils
from mfr.core import extension
from mfr.core import exceptions

from mfr.extensions.unoconv import settings


class UnoconvRenderer(extension.BaseRenderer):

    def __init__(self, url, download_url, file_path, assets_url, ext):
        super().__init__(url, download_url, file_path, assets_url, ext)
        self.base_assets_url = assets_url
        os.makedirs(settings.SHARED_PATH, exist_ok=True)

    def render(self):
        try:
            map = settings.RENDER_MAP[self.ext]
        except KeyError:
            raise exceptions.RendererError('No exporter could be found for the file type requested.', code=400)

        _, file_name = os.path.split(self.file_path)
        shared_file_path = os.path.join(settings.SHARED_PATH, file_name)
        converted_file_ext = '.' + map['format']
        converted_file_path = shared_file_path + converted_file_ext

        extension = utils.make_renderer(
            converted_file_ext,
            self.url,
            self.download_url,
            converted_file_path,
            self.base_assets_url,
            converted_file_ext
        )

        # Due to cross volume movement in unix we leverage shutil.move which properly handles this case.
        # http://bytes.com/topic/python/answers/41652-errno-18-invalid-cross-device-link-using-os-rename#post157964
        shutil.move(self.file_path, shared_file_path)

        try:
            connection_string = 'socket,host={},port={};urp;StarOffice.ComponentContext'.format(settings.ADDRESS, settings.PORT)
            subprocess.check_call(['/usr/bin/unoconv', '-n', '-c', '"' + connection_string + '"', '-f', map['format'], '-o', converted_file_path, '-d', map['doctype'], '-vvv', shared_file_path])
        except subprocess.CalledProcessError:
            raise exceptions.RendererError('Unable to render the requested file, please try again later.', code=400)

        return extension.render()

    @property
    def file_required(self):
        return True

    @property
    def cache_result(self):
        return True
