import os
import http
import asyncio
import codecs

from tornado import web

from mfr.server import utils as server_utils
from mfr.server import settings
from mfr.server.handlers import core

from mfr.core import *
from mfr.ext import ALL_HANDLERS
from mfr.ext.code_pygments import EXTENSIONS as CODE_EXTENSIONS
from mfr.exceptions import MFRError

TRUTH_MAP = {
    'true': True,
    'false': False,
}

@web.stream_request_body
class RenderHandler(core.BaseHandler):

    ACTION_MAP = {
        'HEAD': 'check'
    }

    def get(self):
        self.write({
            'status': 'testing',
            'version': 'mfr.__version__'
        })
