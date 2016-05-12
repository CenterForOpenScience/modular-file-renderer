import os

import furl


try:
    from mfr import settings
except ImportError:
    settings = {}

config = settings.get('SERVER_CONFIG', {})


STATIC_PATH = config.get('STATIC_PATH', os.path.join(os.path.dirname(__file__), 'static'))

ADDRESS = config.get('ADDRESS', '127.0.0.1')
PORT = config.get('PORT', 7778)

DEBUG = config.get('DEBUG', False)

SSL_CERT_FILE = config.get('SSL_CERT_FILE', None)
SSL_KEY_FILE = config.get('SSL_KEY_FILE', None)

XHEADERS = config.get('XHEADERS', False)
CORS_ALLOW_ORIGIN = config.get('CORS_ALLOW_ORIGIN', '*')

CHUNK_SIZE = config.get('CHUNK_SIZE', 65536)  # 64KB
MAX_BUFFER_SIZE = config.get('MAX_BUFFER_SIZE', 1024 * 1024 * 100)  # 100MB

PROVIDER_NAME = config.get('PROVIDER_NAME', 'osf')

CACHE_ENABLED = config.get('CACHE_ENABLED', False)
CACHE_PROVIDER_NAME = config.get('CACHE_PROVIDER_NAME', 'filesystem')
CACHE_PROVIDER_SETTINGS = config.get('CACHE_PROVIDER_SETTINGS', {'folder': '/tmp/mfr/'})
CACHE_PROVIDER_CREDENTIALS = config.get('CACHE_PROVIDER_CREDENTIALS', {})

LOCAL_CACHE_PROVIDER_SETTINGS = config.get('LOCAL_CACHE_PROVIDER_SETTINGS', {'folder': '/tmp/mfrlocalcache/'})

ALLOWED_PROVIDER_DOMAINS = config.get('ALLOWED_PROVIDER_DOMAINS', ['http://localhost:5000/'])
ALLOWED_PROVIDER_NETLOCS = []
for domain in ALLOWED_PROVIDER_DOMAINS:
    ALLOWED_PROVIDER_NETLOCS.append(furl.furl(domain).netloc)
