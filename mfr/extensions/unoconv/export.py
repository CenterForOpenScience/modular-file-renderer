import asyncio
import os

from os.path import (
    basename,
    splitext
)

from mfr.core import extension
from mfr.core import exceptions

from mfr.extensions.unoconv.settings import (
    ADDRESS,
    PORT,
    UNOCONV_BIN,
    UNOCONV_TIMEOUT
)


class UnoconvExporter(extension.BaseExporter):

    async def export(self):
        self.cmd = [
            UNOCONV_BIN,
            '-n',
            '-c', 'socket,host={},port={};urp;StarOffice.ComponentContext'.format(ADDRESS, PORT),
            '-f', self.format,
            '-o', self.output_file_path,
            '-vvv',
            await self.source_file_path
        ]
        self.process = await asyncio.create_subprocess_exec(*self.cmd)
        try:
            stdout, stderr = await asyncio.wait_for(self.process.communicate(), timeout=UNOCONV_TIMEOUT)
        except asyncio.TimeoutError:
            # When this error is raised, the coroutine is also cancelled
            return self.unoconv_fail()
        if self.process.returncode != 0:
            return self.unoconv_fail()

    def unoconv_fail(self):
        """Raise an exception with information that will be necessary for
        debugging.
        """
        path = getattr(self, '_source_file_path', '')
        name, extension = splitext(basename(path))
        raise exceptions.SubprocessError(
            'Unable to export the file in the requested format, please try again later.',
            process='unoconv',
            cmd=str(*self.cmd),
            returncode=self.process.returncode,
            path=str(path),
            code=400,
            extension=extension or '',
            exporter_class='unoconv',
        )
