import pytest
from mfr.core.exceptions import ProviderError

from tornado.httpclient import HTTPError
from tests import utils
from tornado import testing



class TestRenderHandler(utils.HandlerTestCase):

    @testing.gen_test
    def test_format_url(self):

        with pytest.raises(HTTPError) as e:
            yield self.http_client.fetch(self.get_url('/export'), method='GET')
        assert e.value.message == 'Bad Request'
        assert e.value.code == 400

        with pytest.raises(HTTPError) as e:
            yield self.http_client.fetch(self.get_url('/export?format=pdf'), method='GET')
        assert e.value.message == 'Bad Request'
        assert e.value.code == 400

        with pytest.raises(HTTPError) as e:
            yield self.http_client.fetch(self.get_url('/export?url=http://test.com'), method='GET')
        assert e.value.message == 'Bad Request'
        assert e.value.code == 400
