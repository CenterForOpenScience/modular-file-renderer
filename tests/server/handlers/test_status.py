import json
from http import HTTPStatus

from tornado import testing

from mfr.version import __version__

from tests import utils


class TestStatusHandler(utils.HandlerTestCase):
    @testing.gen_test
    def test_get_status(self):
        resp = yield self.http_client.fetch(self.get_url('/status'))

        data = json.loads(resp.body.decode('utf-8'))
        assert resp.code == HTTPStatus.OK
        assert data['status'] == 'up'
        assert data['version'] == __version__
