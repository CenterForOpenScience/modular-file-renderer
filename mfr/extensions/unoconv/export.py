from http import HTTPStatus
from os.path import basename, splitext
from subprocess import run, CalledProcessError

from mfr.core.extension import BaseExporter
from mfr.core.exceptions import SubprocessError
from mfr.extensions.unoconv.settings import (PORT,
                                             ADDRESS,
                                             UNOCONV_BIN,
                                             UNOCONV_TIMEOUT)


class UnoconvExporter(BaseExporter):

    def export(self):
        try:
            run([
                UNOCONV_BIN,
                '-n',
                '-c', 'socket,host={},port={};urp;StarOffice.ComponentContext'.format(ADDRESS, PORT),
                '-f', self.format,
                '-o', self.output_file_path,
                '-vvv',
                self.source_file_path
            ], check=True, timeout=UNOCONV_TIMEOUT)
        except CalledProcessError as err:
            name, extension = splitext(basename(self.source_file_path))
            raise SubprocessError(
                'Unable to export the file in the requested format, please try again later.',
                process='unoconv',
                cmd=str(err.cmd),
                returncode=err.returncode,
                path=str(self.source_file_path),
                code=HTTPStatus.BAD_REQUEST,
                extension=extension or '',
                exporter_class='unoconv',
            )
