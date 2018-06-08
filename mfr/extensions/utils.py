import logging
from typing import Tuple
from urllib.parse import parse_qs, urlencode, urlparse

from mfr.extensions import settings

logger = logging.getLogger(__name__)


def munge_url_for_localdev(url: str) -> Tuple:
    """If MFR is being run in a local development environment (i.e. LOCAL_DEVELOPMENT is True), we
    need to replace the internal host (the one the backend services communicate on, default:
    192.168.168.167) with the external host (the one the user provides, default: "localhost")
    e.g. http://192.168.168.167:7777/foo/bar => http://localhost:7777/foo/bar
    """

    url_obj = urlparse(url)
    if settings.LOCAL_DEVELOPMENT and url_obj.hostname == settings.DOCKER_LOCAL_HOST:
        query_dict = parse_qs(url_obj.query, keep_blank_values=True)

        # the 'mode' param will break image downloads from the osf
        query_dict.pop('mode', None)

        url_obj = url_obj._replace(
            query=urlencode(query_dict, doseq=True),
            netloc='{}:{}'.format(settings.LOCAL_HOST, url_obj.port)
        )

    return url_obj


def escape_url_for_template(url: str, logs: bool=True) -> str:
    """Escape (URL Encode) single and double quote(s) for the given URL.

    Download and export URLs may end up not properly encoded right before they are about to be sent
    to the mako template due to issues including (but not limited to) (1) ``furl`` dropping encoding
    for single quote (2) URL (provided by users or constructed by scripts) not having the correct
    encoding. This helper method must be called for each render request that sends URL to the mako
    template.

    :param str url: the URL to be sent to the mako template
    :param bool logs: whether to enable warnings, default is `True` and is set to `False` for tests
    :return: the properly encoded URL
    """

    safe_url = url.replace('"', '%22').replace("'", '%27')
    if url != safe_url and logs:
        logger.warning('Unsafe URL containing unescaped single (double) quote(s) has been replaced')
    return safe_url
