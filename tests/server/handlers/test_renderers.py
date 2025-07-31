import json
from importlib.metadata import entry_points

from tornado import testing

from tests import utils


class TestRenderersHandler(utils.HandlerTestCase):
    @testing.gen_test
    def test_get_status(self):
        resp = yield self.http_client.fetch(self.get_url("/renderers"))

        renderers = {}
        for ep in entry_points().select(group="mfr.renderers"):
            renderers.update({ep.name: ep.load().__name__})

        data = json.loads(resp.body.decode("utf-8"))
        assert resp.code == 200
        assert data["renderers"] == renderers
