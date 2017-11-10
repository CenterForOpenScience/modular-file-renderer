import json

import pkg_resources
from tornado import testing

from tests import utils


class TestExportersHandler(utils.HandlerTestCase):

    @testing.gen_test
    def test_get_status(self):
        resp = yield self.http_client.fetch(self.get_url('/exporters'))

        exporters = {}
        for ep in pkg_resources.iter_entry_points(group='mfr.exporters'):
            exporters.update({ep.name: ep.load().__name__})

        data = json.loads(resp.body.decode('utf-8'))
        assert resp.code == 200
        assert data['exporters'] == exporters
