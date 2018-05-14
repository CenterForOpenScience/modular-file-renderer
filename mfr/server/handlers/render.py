import asyncio
import logging

from furl import furl
import waterbutler.core.streams
import waterbutler.core.exceptions

from mfr.server import settings
from mfr.core import utils as utils
from mfr.server.handlers import core


logger = logging.getLogger(__name__)

DEFAULT_RENDER = {'renderer': '.pdf', 'format': 'pdf'}

RENDER_MAP = {
    # 'csv': {'renderer': '.xlsx', 'format': 'xlsx'},
    # 'ppt': {'renderer': '.pdf', 'format': 'pdf'},
    # 'pptx': {'renderer': '.pdf', 'format': 'pdf'},
}


class RenderHandler(core.BaseHandler):

    NAME = 'render'
    ALLOWED_METHODS = ['GET']

    async def prepare(self):
        """Set up the handler before actually accepting the request body
        """
        # Bail out early if we don't handle this type of request
        if self.request.method not in self.ALLOWED_METHODS:
            return

        await super().prepare()

        self.renderer_name = utils.get_renderer_name(self.metadata.ext)
        self.cache_file_id = self.metadata.unique_key

    async def get(self):
        """Return HTML that will display the given file.
        This process proceeds as follows:

        1.  Try to get a cached version
        2.  Ensure that the file is a renderable type, else convert it to a
        renderable type.
        3.  Instantiate a renderer capable of rendering the file type and
        render the file
        4.  If the file is cacheable, cache the file.
        """
        if self.render.cache_result and settings.CACHE_ENABLED:
            # Try and use a cached version of the render. If the cached version
            # exists, send it as the response, and return immediately.
            try:
                return await self.write_stream(await self.get_cached_render())
            # No cached version of the render
            except waterbutler.core.exceptions.DownloadError as e:
                self.track_cache_miss(e)

        # Ok so the file needs to be rendered.
        # Is the file in a format that is renderable?
        renderable = ['.pdf']
        if not self.metadata.ext.lower() in renderable:
            # The file is required and it's not a renderable fromat, so it
            # needs to be converted.
            self.convert_file()

        # Perform the render and write the result to the response
        rendition = await self.render()
        await self.write_stream(rendition)

        # Spin off upload of cached render into non-blocking operation
        if self.render.cache_result and settings.CACHE_ENABLED:
            self.cache_result(rendition)

    async def get_cached_render(self):
        """Fetches and returns the response from the cache"""
        cached_render = await self.cache_provider.download(await self.cache_file_path)
        logger.info('Cached file found; Sending downstream [{}]'.format(self.cache_file_path))
        self.metrics.add('cache_file.result', 'hit')
        return cached_render

    def track_cache_miss(self, e):
        """Track and log requests to the cache that are misses"""
        assert e.code == 404, 'Non-404 DownloadError {!r}'.format(e)
        logger.info('No cached file found; Starting render[{}]'.format(self.cache_file_path.result))
        self.metrics.add('cache_file.result', 'miss')

    @property
    def source_stream(self):
        """The stream to use as input. Awaitable in arder to be able
        to pass it around without having to actually download it until it's
        needed.
        """
        try:
            return self._source_stream
        except:
            self._source_stream = self.provider.download()
            return self._source_stream

    @property
    def export_url(self):
        try:
            return self._export_url
        except:
            self._export_url = self.request.uri.replace('/render?', '/export?', 1)
            return self._export_url

    def convert_file(self):
        """The source stream is an awaitable that yields a stream. In order to
        avoid actual download unless it's necessary. this changes the future
        from the original waterbutler-sourced file to the future returned by
        exporting the file.

        Also change the url for the file to an export url
        for the case that the file is not required."""
        try:
            map = RENDER_MAP[self.metadata.ext]
        except KeyError:
            map = DEFAULT_RENDER
        self._source_stream = utils.bind_convert(
            self.metadata,
            self.source_stream,
            map['format']
        )()
        exported_url = furl(self.export_url)
        exported_url.args['format'] = map['format']
        self.metadata.download_url = exported_url.url
        self.url = exported_url.url

    @property
    def render(self):
        """Make a render function that will return the rendered file as a string
        when invoked We need the renderer here because the renderer knows if
        the file is cacheable. It is not ideal to make a cache request if it
        is known a priori the file cannot be cached.

        Make every effort to minimize the requirements of creating the
        rederer; if the file is cached, a faster resonse can be achieved.
        """
        try:
            return self._render
        except:
            self._render = utils.bind_render(
                self.metadata,
                self.source_stream,  # Don't await this- it'll start downloading
                self.url,
                '{}://{}/assets'.format(self.request.protocol, self.request.host),
                self.export_url
            )
            return self._render

    def cache_result(self, rendition):
        return asyncio.ensure_future(
            self.cache_provider.upload(
                waterbutler.core.streams.StringStream(rendition),
                self.cache_file_path
            )
        )
