import subprocess

from mfr.core import extension
from mfr.core import exceptions

from mfr.extensions.unoconv import settings


class UnoconvExporter(extension.BaseExporter):

    def export(self):
        try:
            subprocess.check_call([
                settings.UNOCONV_BIN,
                '-n',
                '-c', 'socket,host={},port={};urp;StarOffice.ComponentContext'.format(settings.ADDRESS, settings.PORT),
                '-f', self.format,
                '-o', self.output_file_path,
                # '-d', map['doctype'],
                '-vvv',
                self.source_file_path
            ])
        except subprocess.CalledProcessError:
            raise exceptions.ExporterError('Unable to export the file in the requested format, please try again later.', code=400)
