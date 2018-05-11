import asyncio
import os
import subprocess

from mfr.core import extension
from mfr.core import exceptions

from mfr.extensions.unoconv import settings


class UnoconvExporter(extension.BaseExporter):

    async def export(self):
        try:
            process = await asyncio.create_subprocess_exec(
                *[
                    settings.UNOCONV_BIN,
                    '-n',
                    '-c', 'socket,host={},port={};urp;StarOffice.ComponentContext'.format(settings.ADDRESS, settings.PORT),
                    '-f', self.format,
                    '-o', self.output_file_path,
                    '-vvv',
                    await self.source_file_path
                ]#,
                #check=True#,
                #timeout=settings.UNOCONV_TIMEOUT
            )
            stdout, stderr = await process.communicate()
        except subprocess.CalledProcessError as err:
            name, extension = os.path.splitext(os.path.split(await self.source_file_path)[-1])
            raise exceptions.SubprocessError(
                'Unable to export the file in the requested format, please try again later.',
                process='unoconv',
                cmd=str(err.cmd),
                returncode=err.returncode,
                path=str(await self.source_file_path),
                code=400,
                extension=extension or '',
                exporter_class='unoconv',
            )
