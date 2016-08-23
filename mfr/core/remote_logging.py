import copy
import json
import logging

import aiohttp
# from geoip import geolite2

import mfr
from mfr.server import settings

# import waterbutler
from waterbutler.core.utils import async_retry


logger = logging.getLogger(__name__)


@async_retry(retries=5, backoff=5)
async def log_analytics(request, metrics):
    """Send events to Keen describing the action that occurred."""
    if settings.KEEN_PRIVATE_PROJECT_ID is None:
        return

    keen_payload = copy.deepcopy(metrics)
    keen_payload['meta'] = {
        'mfr_version': mfr.__version__,
        # 'wb_version': waterbutler.__version__,
        'epoch': 1,
    }
    keen_payload.update(request)
    keen_payload['keen'] = {
        'addons': [
            {
                'name': 'keen:url_parser',
                'input': {
                    'url': 'request.url'
                },
                'output': 'request.info',
            },
            {  # private
                'name': 'keen:ip_to_geo',
                'input': {
                    'ip': 'tech.ip'
                },
                'output': 'geo',
            },
            {  # private
                'name': 'keen:ua_parser',
                'input': {
                    'ua_string': 'tech.ua',
                },
                'output': 'tech.info',
            },
        ],
    }

    if request['referrer']['url'] is not None:
        keen_payload['keen']['addons'].append({
            'name': 'keen:referrer_parser',
            'input': {
                'referrer_url': 'referrer.url',
                'page_url': 'request.url'
            },
            'output': 'referrer.info'
        })
        keen_payload['keen']['addons'].append({
            'name': 'keen:url_parser',
            'input': {
                'url': 'referrer.url'
            },
            'output': 'referrer.info',
        })

    collection = 'mfr_action'

    # send the private payload
    await _send_to_keen(keen_payload, collection, settings.KEEN_PRIVATE_PROJECT_ID,
                        settings.KEEN_PRIVATE_WRITE_KEY, 'private')


async def _send_to_keen(payload, collection, project_id, write_key, domain='private'):
    """Serialize and send an event to Keen.  If an error occurs, try up to five more times.
    Will raise an excpetion if the event cannot be sent."""

    serialized = json.dumps(payload).encode('UTF-8')
    logger.debug("Serialized payload: {}".format(serialized))
    headers = {
        'Content-Type': 'application/json',
        'Authorization': write_key,
    }
    url = '{0}/{1}/projects/{2}/events/{3}'.format(settings.KEEN_API_BASE_URL,
                                                   settings.KEEN_API_VERSION,
                                                   project_id, collection)

    async with await aiohttp.request('POST', url, headers=headers, data=serialized) as resp:
        if resp.status == 201:
            logger.info('Successfully logged {} to {} collection in {} Keen'.format(
                payload['handler']['type'], collection, domain
            ))
        else:
            raise Exception('Failed to log {} to {} collection in {} Keen. Status: {} Error: {}'.format(
                payload['handler']['type'], collection, domain, str(int(resp.status)), await resp.read()
            ))
        return


def _serialize_request(request):
    """Serialize the original request."""
    if request is None:
        return {}

    headers_dict = {}
    for (k, v) in sorted(request.headers.get_all()):
        if k not in ('Authorization', 'Cookie', 'User-Agent',):
            headers_dict[k] = v

    serialized = {
        'tech': {
            'ip': request.remote_ip,
            'ua': request.headers['User-Agent'],
        },
        'request': {
            'method': request.method,
            'url': request.full_url(),
            'time': request.request_time(),
            'headers': headers_dict,
        },
        'referrer': {
            'url': None,
        },
    }

    if 'Referer' in request.headers:
        referrer = request.headers['Referer']
        serialized['referrer']['url'] = referrer

    return serialized
