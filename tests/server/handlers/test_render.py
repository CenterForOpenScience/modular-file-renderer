from tornado import testing

from tests import utils


class TestRenderHandler(utils.HandlerTestCase):
    @testing.gen_test
    def test_options_skips_prepare(self):
        # Would crash b/c lack of mocks
        yield self.http_client.fetch(self.get_url("/render"), method="OPTIONS")
