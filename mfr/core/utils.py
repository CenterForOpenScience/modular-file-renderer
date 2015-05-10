import os
import functools
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

def make_provider(name, url):
    """Returns an instance of :class:`mfr.core.provider.BaseProvider`

    :param str name: The name of the provider to instantiate. (osf)
    :param dict url:

    :rtype: :class:`mfr.core.provider.BaseProvider`
    """
    manager = driver.DriverManager(
        namespace='mfr.providers',
        name=name,
        invoke_on_load=True,
        invoke_args=(url, ),
    )
    return manager.driver

def make_extension(name, url, file_path, assets_url):
    """Returns an instance of :class:`mfr.core.ext.BaseProvider`

    :param str name: The name of the extension to instantiate. (.jpg, .docx, etc)
    :param dict url:
    :param dict file_path:
    :param dict assets_url:

    :rtype: :class:`mfr.core.extension.BaseExtension`
    """
    manager = driver.DriverManager(
        namespace='mfr.extensions',
        name=name,
        invoke_on_load=True,
        invoke_args=(url, file_path, assets_url),
    )
    return manager.driver

def as_task(func):
    if not asyncio.iscoroutinefunction(func):
        func = asyncio.coroutine(func)

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return asyncio.async(func(*args, **kwargs))

    return wrapped


def async_retry(retries=5, backoff=1, exceptions=(Exception, ), raven=client):

    def _async_retry(func):

        @as_task
        @functools.wraps(func)
        def wrapped(*args, __retries=0, **kwargs):
            try:
                return (yield from asyncio.coroutine(func)(*args, **kwargs))
            except exceptions as e:
                if __retries < retries:
                    wait_time = backoff * __retries
                    logger.warning('Task {0} failed, {1} / {2} retries. Waiting {3} seconds before retrying'.format(func, __retries, retries, wait_time))

                    yield from asyncio.sleep(wait_time)
                    return wrapped(*args, __retries=__retries + 1, **kwargs)
                else:
                    # Logs before all things
                    logger.error('Task {0} failed with exception {1}'.format(func, e))

                    if raven:
                        # Only log if a raven client exists
                        client.captureException()

                    # If anything happens to be listening
                    raise e

        # Retries must be 0 to start with
        # functools partials dont preserve docstrings
        return wrapped

    return _async_retry
