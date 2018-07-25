import copy
import json
import logging

import aiohttp

from mfr.server import settings
from mfr.version import __version__
from waterbutler.core.utils import async_retry


logger = logging.getLogger(__name__)


async def log_analytics(request, metrics, is_error=False):
    """Send events to Keen describing the action that occurred."""
    if settings.KEEN_PRIVATE_PROJECT_ID is None:
        return

    keen_payload = copy.deepcopy(metrics)
    keen_payload['meta'] = {
        'mfr_version': __version__,
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
                    'ip': 'tech.ip',
                    'remove_ip_property': True,
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

    # massage file data, if available
    file_metadata = None
    try:
        file_metadata = metrics['provider']['provider_osf']['metadata']['raw']['data']
    except (KeyError, TypeError):
        pass
    else:
        _munge_file_metadata(file_metadata)

    # send the private payload
    private_collection = 'mfr_errors' if is_error else 'mfr_action'
    await _send_to_keen(keen_payload, private_collection, settings.KEEN_PRIVATE_PROJECT_ID,
                        settings.KEEN_PRIVATE_WRITE_KEY, keen_payload['handler']['type'],
                        domain='private')

    if keen_payload['handler']['type'] != 'render' or file_metadata is None or is_error:
        return

    # build and ship the public file stats payload
    public_payload = _build_public_file_payload('view_file', request, file_metadata)
    await _send_to_keen(public_payload, 'file_stats', settings.KEEN_PUBLIC_PROJECT_ID,
                        settings.KEEN_PUBLIC_WRITE_KEY, keen_payload['handler']['type'],
                        domain='public')


@async_retry(retries=5, backoff=5)
async def _send_to_keen(payload, collection, project_id, write_key, action, domain='private'):
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
            logger.info('Successfully logged {} to {} collection in {} Keen'.format(action, collection, domain))
        else:
            raise Exception('Failed to log {} to {} collection in {} Keen. Status: {} Error: {}'.format(
                action, collection, domain, str(int(resp.status)), await resp.read()
            ))
        return


def _scrub_headers_for_keen(payload, MAX_ITERATIONS=10):
    """ Scrub unwanted characters like \\.\\ from the keys in the keen payload """

    scrubbed_payload = {}
    for key in sorted(payload):
        scrubbed_key = key.replace('.', '-')

        # if our new scrubbed key is already in the payload, we need to increment it
        if scrubbed_key in scrubbed_payload:
            for i in range(1, MAX_ITERATIONS + 1):  # try MAX_ITERATION times, then give up & drop it
                incremented_key = '{}-{}'.format(scrubbed_key, i)
                if incremented_key not in scrubbed_payload:  # we found an unused key!
                    scrubbed_payload[incremented_key] = payload[key]
                    break
        else:
            scrubbed_payload[scrubbed_key] = payload[key]

    return scrubbed_payload


def _serialize_request(request):
    """Serialize the original request."""
    if request is None:
        return {}

    headers_dict = {}
    for (k, v) in sorted(request.headers.get_all()):
        if k not in ('Authorization', 'Cookie', 'User-Agent',):
            headers_dict[k] = v

    headers_dict = _scrub_headers_for_keen(headers_dict)
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


def _build_public_file_payload(action, request, file_metadata):
    public_payload = {
        'meta': {
            'epoch': 1,
        },
        'request': {
            'url': request['request']['url']
        },
        'anon': {  # intended for anonymized geolocation, never implemented
            'country': None,
            'continent': None,
        },
        'action': {
            'type': action,
        },
        'file': file_metadata,
        'keen': {
            'addons': [
                {
                    'name': 'keen:url_parser',
                    'input': {
                        'url': 'request.url'
                    },
                    'output': 'request.info',
                },
            ],
        },
    }

    try:
        public_payload['node'] = {'id': file_metadata['resource']}
    except KeyError:
        pass

    if request['referrer']['url'] is not None:
        public_payload['referrer'] = request['referrer']  # .info added via keen addons
        public_payload['keen']['addons'].append({
            'name': 'keen:referrer_parser',
            'input': {
                'referrer_url': 'referrer.url',
                'page_url': 'request.url'
            },
            'output': 'referrer.info'
        })
        public_payload['keen']['addons'].append({
            'name': 'keen:url_parser',
            'input': {
                'url': 'referrer.url'
            },
            'output': 'referrer.info',
        })

    return public_payload


def _munge_file_metadata(metadata):
    if metadata is None:
        return None

    try:
        file_extra = metadata.pop('extra')
    except KeyError:
        pass
    else:
        metadata['extra'] = {
            'common': {},
            metadata['provider']: file_extra,
        }

    # synthetic fields to make Keen queries easier/prettier
    metadata['full_path'] = '/'.join([
        '', metadata['resource'], metadata['provider'], metadata['path'].lstrip('/')
    ])
    metadata['full_materialized'] = '/'.join([
        '', metadata['resource'], metadata['provider'], metadata['materialized'].lstrip('/')
    ])

    return metadata
