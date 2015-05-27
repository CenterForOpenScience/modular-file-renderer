import asyncio

import aiohttp

from stevedore import driver
from raven.contrib.tornado import AsyncSentryClient

from mfr import settings


sentry_dns = settings.get('SENTRY_DSN', None)


class AioSentryClient(AsyncSentryClient):

    def send_remote(self, url, data, headers=None, callback=None):
        headers = headers or {}
        if not self.state.should_try():
            message = self._get_log_message(data)
            self.error_logger.error(message)
            return

        future = aiohttp.request('POST', url, data=data, headers=headers)
        asyncio.async(future)


if sentry_dns:
    client = AioSentryClient(sentry_dns)
else:
    client = None


def make_provider(name, request, url):
    """Returns an instance of :class:`mfr.core.provider.BaseProvider`

    :param str name: The name of the provider to instantiate. (osf)
    :param dict url:

    :rtype: :class:`mfr.core.provider.BaseProvider`
    """
    manager = driver.DriverManager(
        namespace='mfr.providers',
        name=name,
        invoke_on_load=True,
        invoke_args=(request, url, ),
    )
    return manager.driver


def make_exporter(name, file_path, ext, type):
    """Returns an instance of :class:`mfr.core.extension.BaseExporter`

    :param str name: The name of the extension to instantiate. (.jpg, .docx, etc)
    :param dict file_path:
    :param dict ext:
    :param dict type: The exported file type

    :rtype: :class:`mfr.core.extension.BaseExporter`
    """
    manager = driver.DriverManager(
        namespace='mfr.exporters',
        name=name or '<none>',
        invoke_on_load=True,
        invoke_args=(file_path, ext, type),
    )
    return manager.driver


def make_renderer(name, url, file_path, assets_url, ext):
    """Returns an instance of :class:`mfr.core.extension.BaseRenderer`

    :param str name: The name of the extension to instantiate. (.jpg, .docx, etc)
    :param dict url:
    :param dict file_path:
    :param dict assets_url:
    :param dict ext

    :rtype: :class:`mfr.core.extension.BaseRenderer`
    """
    manager = driver.DriverManager(
        namespace='mfr.renderers',
        name=name or '<none>',
        invoke_on_load=True,
        invoke_args=(url, file_path, assets_url, ext, ),
    )
    return manager.driver
