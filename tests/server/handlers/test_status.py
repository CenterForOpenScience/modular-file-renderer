from version import __version__
import json
from tests import utils
from tornado import testing


class TestStatusHandler(utils.HandlerTestCase):
    @testing.gen_test
    def test_get_status(self):
        resp = yield self.http_client.fetch(self.get_url('/status'))

        data = json.loads(resp.body.decode('utf-8'))
        assert resp.code == 200
        assert data['status'] == 'up'
        assert data['version'] == __version__
