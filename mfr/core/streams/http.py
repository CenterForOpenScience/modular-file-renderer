import asyncio

from mfr.core.streams import BaseStream


class ResponseStreamReader(BaseStream):

    def __init__(self, response):
        super().__init__()
        self.response = response
        self.content_type = self.response.headers.get('Content-Type', 'application/octet-stream')

    @property
    def size(self):
        return self.response.headers.get('Content-Length')

    @asyncio.coroutine
    def _read(self, size):
        return (yield from self.response.content.read(size))
