from mfr.server import utils
from mfr.server.handlers import core
from mfr.core_methods import render
from mfr.server.settings import code_extensions
from mfr.tasks import core
from mfr.settings import defaults

import codecs

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
        encoding = None
        if get_file_extensions(self.arguments['file_path']) in code_extensions:
            encoding = 'urf-8'
        with codecs.open(self.arguments['file_path'], encoding=encoding):
        try:
            pass

        # if file is cached
        #    stream back to client
        # if file is not cached
        #    download file from waterbutler
        #    pass to renderer
        #    cache result
        #    stream back to client

        result = yield from self.ext.render(**self.arguments)

        if defaults.USE_CELERY:
            pass
                #rendered_result = build_html(result).delay
        else:
            rendered_result = build_html(result)
        self.write({'data': result})


