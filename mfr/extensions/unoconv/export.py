from http import HTTPStatus
from os.path import basename, splitext

from unoserver.client import UnoClient
from mfr.core.extension import BaseExporter
from mfr.core.exceptions import SubprocessError
from mfr.extensions.unoconv.settings import (
    UNOSERVER_HOST,
    UNOSERVER_PORT,
)


class UnoconvExporter(BaseExporter):
    """
    Uses UnoClient (unoserver) to convert the source file into the requested format.
    """

    def export(self):
        client = UnoClient(
            server=UNOSERVER_HOST,
            port=int(UNOSERVER_PORT),
        )
        try:
            client.convert(
                inpath=self.source_file_path,
                outpath=self.output_file_path,
                convert_to=self.format,
            )
        except Exception as err:
            name, extension = splitext(basename(self.source_file_path))
            raise SubprocessError(
                'Unable to export the file in the requested format, please try again later.',
                process='unoserver',
                cmd=str(err),
                returncode=None,
                path=str(self.source_file_path),
                code=HTTPStatus.BAD_REQUEST,
                extension=extension or '',
                exporter_class='unoserver',
            )
