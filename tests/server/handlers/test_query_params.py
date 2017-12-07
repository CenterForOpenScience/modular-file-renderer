from http import HTTPStatus

import pytest
from tornado import testing
from tornado.httpclient import HTTPError

from tests import utils


class TestQueryParamsHandler(utils.HandlerTestCase):

    @testing.gen_test
    def test_format_url(self):

        with pytest.raises(HTTPError) as e:
            yield self.http_client.fetch(self.get_url('/export'), method='GET')
        assert e.value.message == 'Bad Request'
        assert e.value.code == HTTPStatus.BAD_REQUEST

        with pytest.raises(HTTPError) as e:
            yield self.http_client.fetch(self.get_url('/export?format=pdf'), method='GET')
        assert e.value.message == 'Bad Request'
        assert e.value.code == HTTPStatus.BAD_REQUEST

        with pytest.raises(HTTPError) as e:
            yield self.http_client.fetch(self.get_url('/export?url=http://test.com'), method='GET')
        assert e.value.message == 'Bad Request'
        assert e.value.code == HTTPStatus.BAD_REQUEST
