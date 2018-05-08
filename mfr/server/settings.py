import os

import furl

from mfr import settings


config = settings.child('SERVER_CONFIG')

STATIC_PATH = config.get('STATIC_PATH', os.path.join(os.path.dirname(__file__), 'static'))

ADDRESS = config.get('ADDRESS', 'localhost')
PORT = config.get('PORT', 7778)

DEBUG = config.get_bool('DEBUG', False)

SSL_CERT_FILE = config.get_nullable('SSL_CERT_FILE', None)
SSL_KEY_FILE = config.get_nullable('SSL_KEY_FILE', None)

XHEADERS = config.get_bool('XHEADERS', False)
CORS_ALLOW_ORIGIN = config.get('CORS_ALLOW_ORIGIN', '*')

CHUNK_SIZE = int(config.get('CHUNK_SIZE', 65536))  # 64KB
MAX_BUFFER_SIZE = int(config.get('MAX_BUFFER_SIZE', 1024 * 1024 * 100))  # 100MB

PROVIDER_NAME = config.get('PROVIDER_NAME', 'osf')

CACHE_ENABLED = config.get_bool('CACHE_ENABLED', False)
CACHE_PROVIDER_NAME = config.get('CACHE_PROVIDER_NAME', 'filesystem')
CACHE_PROVIDER_SETTINGS = config.get_object('CACHE_PROVIDER_SETTINGS', {'folder': '/tmp/mfr/'})
CACHE_PROVIDER_CREDENTIALS = config.get_object('CACHE_PROVIDER_CREDENTIALS', {})

LOCAL_CACHE_PROVIDER_SETTINGS = config.get_object('LOCAL_CACHE_PROVIDER_SETTINGS', {'folder': '/tmp/mfrlocalcache/'})

ALLOWED_PROVIDER_DOMAINS = config.get('ALLOWED_PROVIDER_DOMAINS', 'http://localhost:5000/ http://localhost:7777/').split(' ')
ALLOWED_PROVIDER_NETLOCS = []
for domain in ALLOWED_PROVIDER_DOMAINS:
    ALLOWED_PROVIDER_NETLOCS.append(furl.furl(domain).netloc)


analytics_config = config.child('ANALYTICS')

keen_config = analytics_config.child('KEEN')
KEEN_API_BASE_URL = keen_config.get('API_BASE_URL', 'https://api.keen.io')
KEEN_API_VERSION = keen_config.get('API_VERSION', '3.0')

keen_private_config = keen_config.child('PRIVATE')
KEEN_PRIVATE_PROJECT_ID = keen_private_config.get_nullable('PROJECT_ID', None)
KEEN_PRIVATE_WRITE_KEY = keen_private_config.get_nullable('WRITE_KEY', None)

keen_public_config = keen_config.child('PUBLIC')
KEEN_PUBLIC_PROJECT_ID = keen_public_config.get_nullable('PROJECT_ID', None)
KEEN_PUBLIC_WRITE_KEY = keen_public_config.get_nullable('WRITE_KEY', None)
