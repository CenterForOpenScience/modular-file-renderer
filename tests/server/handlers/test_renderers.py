import mfr
import json
from tests import utils
from tornado import testing
import pkg_resources


class TestRenderersHandler(utils.HandlerTestCase):
    @testing.gen_test
    def test_get_status(self):
        resp = yield self.http_client.fetch(self.get_url('/renderers'))

        renderers = {}
        for ep in pkg_resources.iter_entry_points(group='mfr.renderers'):
            renderers.update({ep.name: ep.load().__name__})


        data = json.loads(resp.body.decode('utf-8'))
        assert resp.code == 200
        assert data['renderers'] == renderers
