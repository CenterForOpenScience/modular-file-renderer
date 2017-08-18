import os
import subprocess

import shutil
from tempfile import NamedTemporaryFile
from mfr.core import extension
from mfr.core import exceptions
from mfr.extensions.jsc3d import settings


class JSC3DExporter(extension.BaseExporter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def export(self):
        try:
            # alter original source file with a named temp file, so freecad can read it properly
            with NamedTemporaryFile(mode='w+b') as temp_source_file:
                temp_source_file.name = self.source_file_path + '.step'
                shutil.copy2(self.source_file_path, temp_source_file.name)

                subprocess.check_call([
                    settings.FREECAD_BIN,
                    settings.FREECAD_CONVERT_SCRIPT_BIN,
                    temp_source_file.name,
                    self.output_file_path,
                    # silnce output from freecadcmnd
                ], stdout=subprocess.DEVNULL)

        except subprocess.CalledProcessError as err:
            name, extension = os.path.splitext(os.path.split(self.source_file_path)[-1])
            raise exceptions.SubprocessError(
                'Unable to export the file in the requested format, please try again later.',
                process='freecad',
                cmd=str(err.cmd),
                returncode=err.returncode,
                path=str(self.source_file_path),
                code=400,
                extension=extension or '',
                exporter_class='js3d',
            )
