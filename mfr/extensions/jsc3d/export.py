import shutil
from http import HTTPStatus
from subprocess import (DEVNULL,
                        check_call,
                        TimeoutExpired,
                        CalledProcessError)
from os.path import basename, splitext
from tempfile import NamedTemporaryFile

from mfr.core import exceptions
from mfr.core.extension import BaseExporter
from mfr.extensions.jsc3d.settings import (TIMEOUT,
                                           FREECAD_BIN,
                                           CONVERSION_SCRIPT)


class JSC3DExporter(BaseExporter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def export(self):
        try:
            # alter original source file with a named temp file, so freecad can read it properly
            with NamedTemporaryFile(mode='w+b') as temp_source_file:
                temp_source_file.name = self.source_file_path + '.step'
                shutil.copy2(self.source_file_path, temp_source_file.name)

                check_call(
                    [FREECAD_BIN, CONVERSION_SCRIPT, temp_source_file.name, self.output_file_path],
                    stdout=DEVNULL,  # silence output from freecadcmd
                    timeout=TIMEOUT,
                )

        except CalledProcessError as err:
            name, extension = splitext(basename(self.source_file_path))
            raise exceptions.SubprocessError(
                'Unable to export the file in the requested format, please try again later.',
                process='freecad',
                cmd=str(err.cmd),
                returncode=err.returncode,
                path=str(self.source_file_path),
                code=HTTPStatus.BAD_REQUEST,
                extension=extension or '',
                exporter_class='jsc3d',
            )

        except TimeoutExpired as err:
            name, extension = splitext(basename(self.source_file_path))
            # The return code 52 is not the error code returned by the
            # subprocess, but the error given to it by this waterbutler
            # processs, for timing out.
            raise exceptions.SubprocessError(
                'JSC3D Conversion timed out.',
                code=HTTPStatus.GATEWAY_TIMEOUT,
                process='freecad',
                cmd=str(err.cmd),
                returncode=52,
                path=str(self.source_file_path),
                extension=extension or '',
                exporter_class='jsc3d'
            )
