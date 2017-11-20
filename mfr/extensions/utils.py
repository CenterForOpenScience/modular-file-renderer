from urllib.parse import parse_qs, urlencode, urlparse

from mfr.extensions import settings


def munge_url_for_localdev(func):
    """
    If MFR is being run in a local development environment (i.e. LOCAL_DEVELOPMENT is True), we
    need to replace the internal host (the one the backend services communicate on, default:
    192.168.168.167) with the external host (the one the user provides, default: "localhost")
    e.g. http://192.168.168.167:7777/foo/bar => http://localhost:7777/foo/bar
    """
    def wrapper(self):
        download_url = urlparse(self.metadata.download_url)
        if (settings.LOCAL_DEVELOPMENT and download_url.hostname == settings.DOCKER_LOCAL_HOST):
            query_dict = parse_qs(download_url.query, keep_blank_values=True)
            download_url = download_url._replace(
                query=urlencode(query_dict, doseq=True),
                netloc='{}:{}'.format(settings.LOCAL_HOST, download_url.port)
            )
        self.download_url = download_url
        return func(self)
    return wrapper
