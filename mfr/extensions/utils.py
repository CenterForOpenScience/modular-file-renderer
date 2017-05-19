from urllib.parse import urlparse, parse_qs, urlencode
from mfr.extensions import settings


def download_from_template(func):
    """
    Check if LOCAL_DEVELOPMENT and if so
    Replace the docker domain with localhost (for use in local development).
    e.g. http://localhost:7777/foo/bar => http://192.168.168.167:7777/foo/bar
    """
    def wrapper(self):
        download_url = urlparse(self.metadata.download_url)
        if (settings.LOCAL_DEVELOPMENT and download_url.hostname == settings.DOCKER_LOCAL_HOST):
            query_dict = parse_qs(download_url.query, keep_blank_values=True)
            query_dict.pop('mode', None)
            download_url = download_url._replace(query=urlencode(query_dict, doseq=True))
            download_url = download_url._replace(
                netloc="{}:{}".format(settings.LOCAL_HOST, download_url.port)
            )
        self.download_url = download_url
        return func(self)
    return wrapper
