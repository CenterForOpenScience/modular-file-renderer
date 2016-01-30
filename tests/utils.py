import pytest
import asyncio
from unittest import mock

from decorator import decorator

from tornado import testing
from tornado.platform.asyncio import AsyncIOMainLoop

from mfr.server.app import make_app
from mfr.core.provider import BaseProvider


class MockCoroutine(mock.Mock):
    @asyncio.coroutine
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

@decorator
def async(func, *args, **kwargs):
    future = func(*args, **kwargs)
    asyncio.get_event_loop().run_until_complete(future)


class FakeProvider(BaseProvider):
    pass

class HandlerTestCase(testing.AsyncHTTPTestCase):

    def setUp(self):
        super().setUp()
        # identity_future = asyncio.Future()
        # identity_future.set_result({
        #     'auth': {},
        #     'credentials': {},
        #     'settings': {},
        # })
        # self.mock_identity = mock.Mock()
        # self.mock_identity.return_value = identity_future
        # self.identity_patcher = mock.patch('waterbutler.server.handlers.core.auth_handler.fetch', self.mock_identity)

        # self.mock_provider = MockProvider1({}, {}, {})
        # self.mock_make_provider = mock.Mock(return_value=self.mock_provider)
        # self.make_provider_patcher = mock.patch('waterbutler.core.utils.make_provider', self.mock_make_provider)

        # self.identity_patcher.start()
        # self.make_provider_patcher.start()

    def tearDown(self):
        super().tearDown()
        # self.identity_patcher.stop()
        # self.make_provider_patcher.stop()

    def get_app(self):
        return make_app(debug=False)

    def get_new_ioloop(self):
        return AsyncIOMainLoop()
