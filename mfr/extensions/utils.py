from urllib.parse import parse_qs, urlencode, urlparse

from mfr.extensions import settings


def munge_url_for_localdev(url):
    """
    If MFR is being run in a local development environment (i.e. LOCAL_DEVELOPMENT is True), we
    need to replace the internal host (the one the backend services communicate on, default:
    192.168.168.167) with the external host (the one the user provides, default: "localhost")
    e.g. http://192.168.168.167:7777/foo/bar => http://localhost:7777/foo/bar
    """
    url_obj = urlparse(url)
    if (settings.LOCAL_DEVELOPMENT and url_obj.hostname == settings.DOCKER_LOCAL_HOST):
            query_dict = parse_qs(url_obj.query, keep_blank_values=True)

            # the 'mode' param will break image downloads from the osf
            query_dict.pop('mode', None)

            url_obj = url_obj._replace(
                query=urlencode(query_dict, doseq=True),
                netloc='{}:{}'.format(settings.LOCAL_HOST, url_obj.port)
            )

    return url_obj
