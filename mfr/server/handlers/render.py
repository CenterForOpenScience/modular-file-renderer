import os
import asyncio

from mfr.core import utils as core_utils
from mfr.core.streams.base import StringStream

from mfr.server import utils
from mfr.server import settings
from mfr.server.handlers import core

from mfr.core.streams import FileStreamReader

class RenderHandler(core.BaseHandler):

    ACTION_MAP = {
        'GET': 'render',
    }

    @utils.coroutine
    def prepare(self):
        yield from super().prepare()

    @utils.coroutine
    def get(self):
        """Render a file with the extension"""
        cached_file_path = os.path.join('/tmp', 'mfr', 'files', self.unique_key)
        cached_rendition_path = os.path.join('/tmp', 'mfr', 'rendition', self.unique_key)

        os.makedirs(os.path.dirname(cached_file_path), exist_ok=True)
        os.makedirs(os.path.dirname(cached_rendition_path), exist_ok=True)

        self.extension = core_utils.make_extension(
            self.ext_name,
            self.url,
            cached_file_path,
            '{}://{}/assets'.format(self.request.protocol, self.request.host),
        )

        # TODO: Remove after changed to write to temp folder then move to final destination
        if os.path.exists(cached_rendition_path):
            os.remove(cached_rendition_path)

        if not os.path.exists(cached_rendition_path):
            if self.extension.requires_file:
                if os.path.exists(cached_file_path):
                    os.remove(cached_file_path)

                file_stream = yield from self.provider.download()
                with open(cached_file_path, 'wb') as file_pointer:
                    chunk = yield from file_stream.read(settings.CHUNK_SIZE)
                    while chunk:
                        file_pointer.write(chunk)
                        chunk = yield from file_stream.read(settings.CHUNK_SIZE)

            loop = asyncio.get_event_loop()
            rendition = (yield from loop.run_in_executor(None, self.extension.render))
            rendition_stream = StringStream(rendition)
            with open(cached_rendition_path, 'wb') as file_pointer:
                chunk = yield from rendition_stream.read(settings.CHUNK_SIZE)
                while chunk:
                    file_pointer.write(chunk)
                    chunk = yield from rendition_stream.read(settings.CHUNK_SIZE)

        with open(cached_rendition_path, 'rb') as file_pointer:
            file_stream = FileStreamReader(file_pointer)
            chunk = yield from file_stream.read(settings.CHUNK_SIZE)
            while chunk:
                self.write(chunk)
                yield from utils.future_wrapper(self.flush())
                chunk = yield from file_stream.read(settings.CHUNK_SIZE)
