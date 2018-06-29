import os
import subprocess

from mfr.core import extension
from mfr.core import exceptions

from mfr.extensions.unoconv import settings


class UnoconvExporter(extension.BaseExporter):

    def export(self):
        try:
            subprocess.run([
                settings.UNOCONV_BIN,
                '-n',
                '-c', 'socket,host={},port={};urp;StarOffice.ComponentContext'.format(settings.ADDRESS, settings.PORT),
                '-f', self.format,
                '-o', self.output_file_path,
                '-vvv',
                self.source_file_path
            ], check=True, timeout=settings.UNOCONV_TIMEOUT)

        except subprocess.CalledProcessError as err:
            name, extension = os.path.splitext(os.path.split(self.source_file_path)[-1])
            raise exceptions.SubprocessError(
                'Unable to export the file in the requested format, please try again later.',
                process='unoconv',
                cmd=str(err.cmd),
                returncode=err.returncode,
                path=str(self.source_file_path),
                code=400,
                extension=extension or '',
                exporter_class='unoconv',
            )
