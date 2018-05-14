from asyncio import (
    TimeoutError,
    create_subprocess_exec,
    wait_for
)
from asyncio.subprocess import (
    DEVNULL
)
from os.path import (
    basename,
    splitext
)
import shutil
import subprocess
from http import HTTPStatus
from tempfile import NamedTemporaryFile

from mfr.core import exceptions
from mfr.core.extension import BaseExporter
from mfr.extensions.jsc3d.settings import (
    FREECAD_BIN,
    TIMEOUT,
    FREECAD_CONVERT_SCRIPT
)


class JSC3DExporter(BaseExporter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def export(self):
        # alter original source file with a named temp file, so freecad can read it properly
        with NamedTemporaryFile(mode='w+b') as temp_source_file:
            temp_source_file.name = await self.source_file_path + '.step'
            shutil.copy2(await self.source_file_path, temp_source_file.name)
            self.cmd = [
                FREECAD_BIN,
                FREECAD_CONVERT_SCRIPT,
                temp_source_file.name,
                self.output_file_path,
                # silence output from freecadcmd
            ]
            self.process = await create_subprocess_exec(*self.cmd, stdout=DEVNULL)
            try:
                stdout, stderr = await wait_for(self.process.communicate(), timeout=TIMEOUT)
            except TimeoutError:
                return self.jsc3d_fail()
            if self.process.returncode != 0:
                return self.jsc3d_fail()

    def jsc3d_fail(self):
        path = getattr(self, '_source_file_path', '')
        name, extension = splitext(basename(path))
        raise exceptions.SubprocessError(
            'Unable to export the file in the requested format, please try again later.',
            process='freecad',
            cmd=str(*self.cmd),
            returncode=self.process.returncode,
            path=str(path),
            code=HTTPStatus.BAD_REQUEST,
            extension=extension or '',
            exporter_class='jsc3d',
        )
