import json
import time
import asyncio

import aiohttp
import tornado.web

from mfr.core import utils
from raven.contrib.tornado import SentryMixin

class BaseHandler(tornado.web.RequestHandler, SentryMixin):

    ACTION_MAP = {}

    def initialize(self):
        method = self.get_query_argument('method', None)
        if method:
            self.request.method = method.upper()

    def set_status(self, code, reason=None):
        return super().set_status(code, reason or HTTP_REASONS.get(code))

    @asyncio.coroutine
    def prepare(self):
        pass

    @utils.async_retry(retries=5, backoff=5)
    def _send_hook(self, fp):
        resp = aiohttp.request(
        'HEAD',
        WATERBUTLER_URL,
        fp
        )
        return resp
