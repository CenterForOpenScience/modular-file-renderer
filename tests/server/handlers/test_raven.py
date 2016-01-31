from unittest import mock
from tornado import testing, web
from raven.contrib.tornado import SentryMixin, AsyncSentryClient


class TornadoAsyncClientTestCase(testing.AsyncHTTPTestCase):

    @web.stream_request_body
    class AnErrorProneStreamingHandler(SentryMixin, web.RequestHandler):
        def get(self):
            try:
                raise Exception("Damn it!")
            except Exception:
                self.captureException(True)

    def get_app(self):
        app = web.Application([
            web.url(r'/a-streaming-error', self.AnErrorProneStreamingHandler),
        ])
        app.sentry_client = AsyncSentryClient(
            'http://public_key:secret_key@host:9000/project'
        )
        return app

    @mock.patch('raven.contrib.tornado.AsyncSentryClient.send_encoded')
    def test_streaming_error_handler(self, send_encoded):
        response = self.fetch('/a-streaming-error?qs=qs')
        self.assertEqual(response.code, 200)
        self.assertEqual(send_encoded.call_count, 1)
        encoded = send_encoded.call_args[0][0]
        decoded = self._app.sentry_client.decode(encoded)

        assert 'user' in decoded
        assert 'request' in decoded
        assert 'exception' in decoded

        http_data = decoded['request']
        self.assertEqual(http_data['cookies'], None)
        self.assertEqual(http_data['url'], response.effective_url)
        self.assertEqual(http_data['query_string'], 'qs=qs')
        self.assertEqual(http_data['method'], 'GET')

        user_data = decoded['user']
        self.assertEqual(user_data['is_authenticated'], False)
